# -*- coding: utf-8 -*-
{
    'name': 'Geo Location Capture',
    'version': '1.0',
    'summary': 'Captura de ubicación por navegador',
    'author': 'Drako Tech Solutions',
    'category': 'Tools',
    'depends': ['base', 'web'],
    'data': [
        'views/geo_location_view.xml',
        'security/ir.model.access.csv',
    ],
    'assets': {
        'web.assets_backend': [
            'geo_location_capture/static/src/js/geo_capture.js',
            'geo_location_capture/static/src/js/geo_button.js',
            'geo_location_capture/static/src/xml/geo_button.xml',
        ],
    },
    'installable': True,
    'application': True,
}
