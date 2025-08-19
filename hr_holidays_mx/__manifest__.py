{
    'name': 'Time Off Custom',
    'version': '1.0',
    'depends': ['hr_holidays', 'hr'],
    'author': 'Tu Empresa',
    'category': 'Human Resources',
    'summary': 'Personalización del módulo de Ausencias y Vacaciones',
    'data': [        
        'views/hr_leave_views.xml',
        'data/hr_employee_cron.xml',
        'views/hr_employee_views.xml',
    ],
    'installable': True,
}
