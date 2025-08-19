{
    'name': 'HR Attendance Tracker',
    'version': '1.0.0',
    'category': 'Human Resources',
    'summary': 'Sistema de seguimiento de asistencia con botones de pausa/reanudación',
    'description': """
        Sistema avanzado de seguimiento de asistencia que permite:
        - Pausar y reanudar el sistema desde el systray
        - Interfaz integrada con los estilos de Odoo
        - Notificaciones en tiempo real
        - Gestión de estado consistente
    """,
    'author': 'Tu Nombre',
    'depends': [
        'base',
        'web',
        'hr_attendance',
    ],
    'data': [
        # Vistas y datos XML si los tienes
        # 'views/hr_button_systray.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # JavaScript
            'hr_button_systray/static/src/js/systray_buttons.js',
            
            # CSS
            'hr_button_systray/static/src/css/systray_buttons.css',
            
            # Plantillas XML
            'hr_button_systray/static/src/xml/systray_buttons.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}