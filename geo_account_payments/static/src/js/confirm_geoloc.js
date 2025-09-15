/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

console.log("Loaded geo_capture_payment.js");

export class CurrentLocation extends Component {
    setup() {
        this.state = useState({
            loading: false,
        });
        this.orm = useService("orm");
        this.action = useService("action");

        this.userId = this.props.action.context.active_id;
        this.getLocation();
        
    }

    async getLocation() {
        if (!navigator.geolocation) {
            alert("Geolocation is not supported by your browser.");
            this.redirectToForm();
            return;
        }

        this.state.loading = true;

        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;

                try {
                    await this.orm.call(
                        'account.payment',
                        'update_coordinates',
                        [[this.userId], lat, lon],
                        { context: this.env.context }
                    );
                    //alert(`Pago generado correctamente`);
                } catch (e) {
                    alert("Failed to update location on server.");
                } finally {
                    this.state.loading = false;
                    this.redirectToForm();
                }
            },
            async (error) => {
                alert(`Error getting location: ${error.message}`);
                this.state.loading = false;
                this.redirectToForm();
            }
        );
    }

    redirectToForm() {
        this.env.config.historyBack();
    }
        
}

CurrentLocation.template = "geo_location_payment.CurrentLocationTemplate";

registry.category("actions").add("geo_location_payment.current_location_action", CurrentLocation);
