# -*- coding: utf-8 -*-
# hr_attendance_sesametime_button/__manifest__.py
{
    'name': 'Attendance Button Sesametime Style (Green/Red)',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Applies Sesametime-like styling with dynamic green/red colors to the Odoo attendance button.',
    'description': """
        This module customizes the main attendance check-in/out button in Odoo,
        making it larger, prominent, and dynamically displaying 'Entrada' (green)
        or 'Salida' (red) based on the current attendance state, mimicking a Sesametime style.
    """,
    'author': 'JOSE GARCIA GARCIA', # ¡Cambia esto por tu nombre o el de tu empresa!
    'depends': ['hr_attendance', 'web'],
    'data': [
        'views/attendance_button_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hr_attendance_sesametime_button/static/src/scss/sesametime_button.scss',
            'hr_attendance_sesametime_button/static/src/js/sesametime_attendance_patch.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}