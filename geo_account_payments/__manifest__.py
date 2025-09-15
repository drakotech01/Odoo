# -*- coding: utf-8 -*-
{
    'name': 'Geolocalización en Pagos (OpenCage)',
    'version': '1.0',
    'summary': 'Registra ubicación al confirmar pagos usando OpenCage',
    'category': 'Accounting',
    'author': 'Tu Nombre o Empresa',
    # Requiere el módulo que tiene el método de geolocalización
    'depends': ['account', 'web'],
    'data': [
        'views/actions.xml',  # Acción cliente para obtener ubicación
        'views/account_payment_views.xml',  # Vista personalizada
    ],
    'assets': {
        'web.assets_backend': [
            'geo_account_payments/static/src/js/confirm_geoloc.js',
            'geo_account_payments/static/src/xml/geo_capture_templates.xml',

        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
