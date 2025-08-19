{
    'name': 'Custom Check-In Systray',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Duplica el botón de check-in en el systray con estilo personalizado',
    'depends': ['web', 'hr_attendance', 'hr'],
    'data': [        
        'views/hr_attendance_views.xml',
        'views/hr_attendance_break_views.xml',
        'security/ir.model.access.csv',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_checkin_systray/static/src/js/custom_checkin_systray.js',
            'custom_checkin_systray/static/src/css/custom_checkin_systray.css',
            'custom_checkin_systray/static/src/xml/custom_checkin_systray.xml',            
        ],
    },
}
