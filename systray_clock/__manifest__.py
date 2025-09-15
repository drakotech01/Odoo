{
    'name': 'Systray Clock',
    'version': '1.0',
    'summary': 'Muestra la hora actual en el systray de Odoo',
    'description': """
        Este módulo agrega un reloj en tiempo real en la barra de systray de Odoo
        que muestra la hora actual del servidor.
        
        Características:
        - Muestra la hora en formato HH:MM:SS
        - Actualización en tiempo real cada segundo
        - Diseño responsivo siguiendo los estándares de Odoo
        - Implementado con OWL para máximo rendimiento
    """,
    'author': 'Tu Nombre',
    'website': 'https://www.tu-sitio.com',
    'category': 'Productivity',
    'depends': ['web'],
    'data': [
    ],
    'assets': {
        'web.assets_backend': [
            'systray_clock/static/src/js/systray_clock.js',
            'systray_clock/static/src/xml/systray_clock.xml',
            'systray_clock/static/src/scss/systray_clock.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}