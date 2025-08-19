{
    'name': 'Auto Close Sessions and Check-ins',
    'version': '1.0',
    'summary': 'Cierra check-ins abiertos y sesiones inactivas automáticamente',
    'description': """
        Este módulo cierra automáticamente los check-ins de asistencia abiertos a las 23:59
        y cierra sesiones de usuarios después de un período de inactividad.
    """,
    'author': 'Tu Nombre',
    'depends': ['base', 'hr_attendance', 'bus'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
    ],
    'post_init_hook': 'post_install_hook',
    'installable': True,
    'application': False,
}