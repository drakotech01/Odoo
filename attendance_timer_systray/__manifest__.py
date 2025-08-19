{
    "name": "Attendance Timer Systray",
    "version": "1.0",
    "author": "Drako Tech Solutions",
    "website": "https://drakotechsolutions.com",
    "category": "Human Resources",
    "license": "LGPL-3",
    "summary": "Temporizador en systray que inicia al hacer Check In",
    "depends": ["hr_attendance", "web"],
    "data": [        
    ],
    "assets": {
        "web.assets_backend": [
            "attendance_timer_systray/static/src/js/attendance_timer_systray.js",
            "attendance_timer_systray/static/src/xml/attendance_timer_systray.xml",
        ],
    },
    "installable": True,
    "application": False,
}
