{
    "name": "HR Attendance Breaks (Enhanced)",
    "version": "1.1.0",
    "summary": "Registro de pausas (comida) en hr.attendance con API y extensibilidad",
    "description": "Añade registros de pausa a hr.attendance, botones en systray, endpoints RPC/HTTP y hooks para extender a otros modelos.",
    "author": "Drako Tech Solutions",
    "category": "Human Resources",
    "depends": ["hr_attendance", "web"],
    "data": [
        #"security/security.xml",
        #"security/ir.model.access.csv",
        #"views/hr_attendance_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "custom_systray/static/src/js/pause_systray.js",
            "custom_systray/static/src/scss/pause_systray.scss",
            "custom_systray/static/src/xml/pause_systray.xml",
        ]
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}