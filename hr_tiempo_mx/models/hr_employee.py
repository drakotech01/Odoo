from odoo import models, fields, api
from datetime import datetime, date

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    leave_ids = fields.One2many('hr.leave', 'employee_id', string='Solicitudes de tiempo libre')
    vacation_days_available = fields.Float('Días de vacaciones disponibles', default=0)
    vacation_days_used = fields.Float('Días de vacaciones usados', compute='_compute_vacation_days_used')
    birthday_leave_used = fields.Boolean('Día de cumpleaños usado este año', compute='_compute_birthday_leave_used')
    time_off_responsible_id = fields.Many2one('res.users', 'Responsable de Tiempo Libre')

    @api.depends('leave_ids', 'leave_ids.state', 'leave_ids.holiday_status_id')
    def _compute_vacation_days_used(self):
        for employee in self:
            employee.vacation_days_used = sum(
                (leave.request_date_to - leave.request_date_from).days + 1 
                for leave in employee.leave_ids
                if leave.holiday_status_id.leave_category == 'vacation' 
                and leave.state in ['validate', 'validate1']
            )

    @api.depends('leave_ids', 'leave_ids.state', 'leave_ids.holiday_status_id', 'leave_ids.request_date_from')
    def _compute_birthday_leave_used(self):
        current_year = datetime.now().year
        for employee in self:
            employee.birthday_leave_used = any(
                leave.holiday_status_id.leave_category == 'birthday' and
                leave.state in ['validate', 'validate1'] and
                leave.request_date_from.year == current_year
                for leave in employee.leave_ids
            )