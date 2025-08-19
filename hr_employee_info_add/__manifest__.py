{
    'name': 'Informacion Adicional de Empleados',
    'version': '1.0',
    'summary': 'Cálculo días de vacaciones y Nombre completo según leyes mexicanas',
    'description': 'Agrega campos personalizados y cálculo automático de vacaciones conforme a la Ley Federal del Trabajo en México.',
    'category': 'Human Resources',
    'author': 'Drako Tech Solutions',
    'depends': ['hr'],
    'data': [
        'views/hr_employee_views.xml',
    ],

    'assets': {
    'web.assets_backend': [
        'hr_employee_info_add/static/src/css/vacaciones_style.css',
        ],
    },

    'installable': True,
    'auto_install': False,
    'application': False,
}
