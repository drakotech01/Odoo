/** @odoo-module **/

import { registry } from "@web/core/registry";
import { CharField } from "@web/views/fields/char/char_field";
import { loadJS, loadCSS } from "@web/core/assets";
import { session } from "@web/session";
import {
    useEffect,
    useRef,
    useState,
    onWillStart,
    onWillUnmount,
} from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

const apiTilesRouteWithToken =
    "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}";
const apiTilesRouteWithoutToken = "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png";

const mapTileAttribution = `
    © <a href="https://www.mapbox.com/about/maps/">Mapbox</a>
    © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>
    <strong>
        <a href="https://www.mapbox.com/map-feedback/" target="_blank">
            Improve this map
        </a>
    </strong>`;

export class MapField extends CharField {
    static template = "dh_map_widget.MapField";
    static props = {
        ...standardFieldProps, // Include standard field props
        latitudeField: { type: String, optional: false },
        longitudeField: { type: String, optional: false },
        enableSearch: { type: Boolean, optional: true },
        readOnly: { type: Boolean, optional: true },
    };
    static defaultProps = {
        enableSearch: false,
        readOnly: false,
    };
    
    setup() {
        super.setup();        
        
        // Show error if required fields are missing
        if (!this.props.latitudeField || !this.props.longitudeField) {
            console.error('MapField: latitudeField and longitudeField props are required');
            return;
        }
        
        onWillStart(() =>
            Promise.all([
                // enterprise
                // loadJS("/web_map/static/lib/leaflet/leaflet.js"),
                // loadCSS("/web_map/static/lib/leaflet/leaflet.css"),
                
                // Community
                loadJS("https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"),
                loadCSS("https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"),
            ])
        );
        
        this.leafletMap = null;
        this.marker = null;
        this.mapContainerRef = useRef("openStreetMap");
        this.mapSearchRef = useRef("mapSearchField"); 
        this.mapSearchResultRef = useRef("mapSearchResult"); 
        this.state = useState({
            closedGroupIds: [],
            expendedPinList: false,
            isMapInitialized: false,
        });
        this.searchHandler = null;
        this.nextId = 1;

        onWillUnmount(() => {
            if (this.searchHandler && this.mapSearchRef.el) {
                this.mapSearchRef.el.removeEventListener('keyup', this.searchHandler);
            }
            if (this.leafletMap) {
                this.leafletMap.remove();
            }
        });

        useEffect(
            () => {
                if (this.mapContainerRef.el && !this.leafletMap && !this.state.isMapInitialized) {
                    this.initializeMap();
                    this.setupMapInteractions();
                    if (this.props.enableSearch && !this.props.readOnly) {
                        this.setupSearch();
                    }
                    this.state.isMapInitialized = true;
                }
            },
            () => [this.mapContainerRef.el]
        );           
    }

    /**
     * Initialize the Leaflet map
     */
    initializeMap() {
        // Use the field names from props
        const lat = this.props.record.data[this.props.latitudeField] || 0;
        const lng = this.props.record.data[this.props.longitudeField] || 0;
        
        this.leafletMap = L.map(this.mapContainerRef.el, {
            maxBounds: [L.latLng(180, -180), L.latLng(-180, 180)],
            center: [lat, lng],
            zoom: 6
        });
        
        L.tileLayer(this.apiTilesRoute, {
            attribution: mapTileAttribution,
            tileSize: 512,
            zoomOffset: -1,
            minZoom: 2,
            maxZoom: 19,
            accessToken: session.map_box_token || "sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=",
        }).addTo(this.leafletMap);
        
        if (lat !== 0 && lng !== 0) {
            this.marker = L.marker([lat, lng]).addTo(this.leafletMap);
        } else {
            this.marker = L.marker([0, 0]);
        }
    }

    /**
     * Setup map click interactions
     */
    setupMapInteractions() {
        if (this.props.readOnly) {
            return;
        }

        this.leafletMap.addEventListener('click', (e) => {
            const newLat = e.latlng.lat;
            const newLng = e.latlng.lng;
            
            if (this.marker) {
                this.marker.setLatLng([newLat, newLng]);
                if (!this.leafletMap.hasLayer(this.marker)) {
                    this.marker.addTo(this.leafletMap);
                }
            } else {
                this.marker = L.marker([newLat, newLng]).addTo(this.leafletMap);
            }
            
            this.props.record.update({
                [this.props.latitudeField]: newLat,
                [this.props.longitudeField]: newLng,
            });
        });
    }

    /**
     * Setup search functionality
     */
    setupSearch() {
        if (!this.mapSearchRef.el) return;

        if (this.searchHandler) {
            this.mapSearchRef.el.removeEventListener('keyup', this.searchHandler);
        }

        this.searchHandler = this.debounce(async (e) => {
            const address = this.mapSearchRef.el.value.trim();
            if (!address) {
                this.mapSearchResultRef.el.innerHTML = '';
                return;
            }

            try {
                const locations = await this.searchLocation(address);
                this.displaySearchResults(locations);
            } catch (error) {
                console.error('Search error:', error);
                this.mapSearchResultRef.el.innerHTML = '<div class="w-100 border-bottom py-2 text-muted">Search failed</div>';
            }
        }, 300);

        this.mapSearchRef.el.addEventListener('keyup', this.searchHandler);
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    async searchLocation(address) {
        const apiUrl = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`;
        const response = await fetch(apiUrl, {
            method: "GET",
            headers: {
                "Accept": "application/json",
            },
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    }

    displaySearchResults(locations) {
        this.mapSearchResultRef.el.innerHTML = '';
        
        if (locations.length === 0) {
            const noResults = document.createElement('div');
            noResults.classList = "w-100 border-bottom py-2 text-muted";
            noResults.textContent = "No results found";
            this.mapSearchResultRef.el.appendChild(noResults);
            return;
        }

        locations.forEach(loc => {
            const locDiv = document.createElement('div');
            locDiv.classList = "w-100 border-bottom py-2 cursor-pointer";
            locDiv.style.cursor = "pointer";
            locDiv.textContent = loc.display_name;
            
            locDiv.addEventListener('click', () => {
                const lat = parseFloat(loc.lat);
                const lng = parseFloat(loc.lon);
                
                if (this.marker) {
                    this.marker.setLatLng([lat, lng]);
                    if (!this.leafletMap.hasLayer(this.marker)) {
                        this.marker.addTo(this.leafletMap);
                    }
                } else {
                    this.marker = L.marker([lat, lng]).addTo(this.leafletMap);
                }
                
                if (!this.props.readOnly) {
                    this.props.record.update({
                        [this.props.latitudeField]: lat,
                        [this.props.longitudeField]: lng,
                    });
                }
                
                this.leafletMap.setView([lat, lng], 12);
                
                this.mapSearchRef.el.value = '';
                this.mapSearchResultRef.el.innerHTML = '';
            });
            
            this.mapSearchResultRef.el.appendChild(locDiv);
        });
    }

    get apiTilesRoute() {
        return session.map_box_token 
            ? apiTilesRouteWithToken
            : apiTilesRouteWithoutToken;
    }
}

export const mapField = {
    component: MapField,
    supportedOptions: [
        {
            label: "Latitude field name (Required)",
            name: "latitude_field",
            type: "string",
        },
        {
            label: "Longitude field name (Required)",
            name: "longitude_field",
            type: "string",
        },
        {
            label: "Enable search functionality",
            name: "enable_search",
            type: "boolean",
            default: false,
        },
        {
            label: "Disable editing (read-only mode)",
            name: "readonly",
            type: "boolean",
            default: false,
        },
    ],
    supportedTypes: ["char"],
    extractProps: ({ options }) => ({
        latitudeField: options.latitude_field,
        longitudeField: options.longitude_field,
        enableSearch: options.enable_search,
        readOnly: options.readonly,
    }),
};

registry.category("fields").add("map", mapField);
