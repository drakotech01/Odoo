{
    "name": "HR Time Work MX - Header Timer",
    "version": "1.0",
    "category": "Human Resources",
    "depends": ["web", "hr_attendance"],
    "data": [
        #"views/webclient_inherit.xml",
        #"views/attendance_timer_systray_templates.xml",
    ],
    "assets": {
        "web.assets_backend": [
            'hr_time_work_mx/static/src/js/attendance_menu_worktime.js',
            "hr_time_work_mx/static/src/js/systray_clock.js",
            #'hr_time_work_mx/static/src/js/systray_worktime.js',
            'hr_time_work_mx/static/src/xml/attendance_menu_worktime.xml',
            "hr_time_work_mx/static/src/xml/systray_clock.xml",
            #'hr_time_work_mx/static/src/xml/systray_worktime.xml',            
            "hr_time_work_mx/static/src/css/systray_clock.css",
            'hr_time_work_mx/static/src/css/systray_widgets.css',
        ],
    },
    "installable": True,
    "application": False,
}
