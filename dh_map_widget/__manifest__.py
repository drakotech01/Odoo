# -*- coding: utf-8 -*-
###############################################################################
#
#    Digital Harbor, Open Source Management Solution
#    Copyright (C) 2024 - Present Digital Harbor (<https://digitalharbor.com.sa>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    'name': "Map Field Widget",
    'summary': """
        Advanced Map Field Widget with interactive mapping capabilities
        for location selection and visualization""",
    
    'description': """
        Map Field Widget
        ================
        
        This module provides an advanced map widget for Odoo that allows:
        - Interactive map-based location selection
        - Address search and geocoding functionality
        - Customizable field mapping for latitude/longitude storage
        - Read-only map display mode
        - Responsive design with multiple map providers support
        
        Features:
        ---------
        • Leaflet.js integration for powerful mapping
        • OpenStreetMap and MapBox support
        • Address search using Nominatim API
        • Customizable field name mapping
        • Configurable search and edit modes
    """,
    
    'author': "Digital Harbor",
    'website': "https://digitalharbor.com.sa",
    'category': 'Extra Tools',
    'version': '18.0.1.0.0',
    'depends': [],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    # 'price': 0.00,
    # 'currency': 'USD',
    'images': ['static/description/banner.jpg'],
    'assets': {
        'web.assets_backend': [
            'dh_map_widget/static/src/*.css',
            'dh_map_widget/static/src/*.xml',
            'dh_map_widget/static/src/*.js',
        ],
    },
    'support': 'support@digitalharbor.com.sa',
    'maintainers': ['Digital Harbor Team'],
}
