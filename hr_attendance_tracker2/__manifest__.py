{
    'name': 'Botones de Pausar/Reanudar en el Systray',
    'version': '1.0',
    'category': 'Extra Tools',
    'summary': 'Añade botones de Pausar y Reanudar al Systray de Odoo',
    'depends': ['web', 'hr_attendance'],
    'assets': {
        'web.assets_backend': [
            # Se añade la ruta a los archivos funcionales
            'hr_attendance_tracker2/static/src/js/systray_buttons.js',
            'hr_attendance_tracker2/static/src/xml/systray_buttons.xml',
        ],
    },
    'license': 'LGPL-3',
}