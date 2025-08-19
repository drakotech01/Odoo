{
    'name': 'Asistencias Extendidas',
    'version': '1.0',
    'summary': 'Extiende asistencias para agregar datos de empleado, retardo, estado y reporte en Excel',
    'author': 'Tu Empresa',
    'category': 'Human Resources',
    'depends': ['hr_attendance', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_attendance_view.xml',
        'data/ir_config_parameter.xml',        
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
