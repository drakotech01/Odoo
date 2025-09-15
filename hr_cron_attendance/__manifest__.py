{
    'name': 'Cierre Automático de Asistencias',
    'version': '1.0',
    'summary': 'Cierra automáticamente registros de asistencia de días anteriores',
    'category': 'Human Resources',
    'author': 'Tu Nombre',
    'website': 'https://www.tuempresa.com',
    'depends': ['hr_attendance'],
    'data': [
        #'views/hr_attendance_views.xml',
        'data/attendance_cron_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}