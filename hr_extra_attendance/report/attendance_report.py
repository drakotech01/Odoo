from odoo import models
import datetime

class AttendanceXlsx(models.AbstractModel):
    _name = 'report.hr_extra_attendance.report_attendance_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        # Creamos una hoja nueva
        sheet = workbook.add_worksheet('Asistencias')
        bold = workbook.add_format({'bold': True})

        # Cabeceras de columna
        headers = ['Nombre', 'Apellido Paterno', 'Apellido Materno', 
                   'Fecha Entrada', 'Hora Entrada', 'Retardo', 'Estado']
        for col, val in enumerate(headers):
            sheet.write(0, col, val, bold)

        # Escribimos los registros
        for row, obj in enumerate(objs, start=1):
            sheet.write(row, 0, obj.name_mx) #Nombre
            sheet.write(row, 1, obj.ap_pat_mx) # Apellido Paterno
            sheet.write(row, 2, obj.ap_mat_mx) # Apellido Materno
            # Convertimos la fecha y hora a formato legible
            sheet.write(row, 3, str(obj.check_in_date or ''))  # Fecha separada
            sheet.write(row, 4, str(obj.check_in_time or ''))  # Hora separada
            sheet.write(row, 5, 'Sí' if obj.is_late else 'No')
            sheet.write(row, 6, obj.status)
