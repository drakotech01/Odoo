{
    'name': 'Spreadsheet Dashboard',
    'version': '18.0.1.0.0',
    'category': 'Tools',
    'summary': 'Gestión de hojas de cálculo con dashboard, gráficos y exportación.',
    'author': 'Drako Tech Solutions, OCA',
    'website': 'https://drakotech.mx',
    'license': 'AGPL-3',
    'depends': ['web', 'base', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'views/spreadsheet_views.xml',
        'report/spreadsheet_report.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'spreadsheet_app/static/src/js/spreadsheet_widget.js',
        ]
    },
    'application': True,
    'installable': True,
}