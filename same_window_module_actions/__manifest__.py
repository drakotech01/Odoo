# -*- coding: utf-8 -*-
{
    'name': "Mantener Ventana Actual en Acciones de Módulos",
    'summary': """Mantiene la ventana actual al activar/actualizar/desinstalar módulos""",
    'description': """
        Modifica el comportamiento de los botones de gestión de módulos para que:
        - Al activar un módulo permanezca en la misma ventana
        - Al actualizar un módulo permanezca en la misma ventana
        - Al desinstalar un módulo permanezca en la misma ventana
    """,
    'author': "Drako Tech Solutions",
    'website': "https://tusitio.com",
    'category': 'Tools',
    'version': '1.0',
    'depends': ['base', 'web'],
    'data': [
        'controllers/main.py',
    ],
    
    'assets': {
        'web.assets_backend': [
            'same_window_module_actions/static/src/js/module_actions.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}