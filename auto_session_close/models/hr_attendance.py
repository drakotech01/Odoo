from odoo import models, fields, api
import datetime

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'
    
    auto_closed = fields.Boolean(string="Cerrado Automáticamente", default=False)

    @api.model
    def close_open_checkins(self):
        open_attendances = self.search([('check_out', '=', False)])
        
        for attendance in open_attendances:
            # Crear datetime a las 23:59 del día del check-in
            check_in_date = attendance.check_in.date()
            check_out_time = datetime.datetime.combine(
                check_in_date,
                datetime.time(23, 59, 0)
            )
            attendance.write({
                'check_out': check_out_time,
                'auto_closed': True
            })
        return True