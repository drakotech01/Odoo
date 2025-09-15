from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HolidaysMigrationWizard(models.TransientModel):
    _name = 'hr.holidays.migration.wizard'
    _description = 'Asistente para migración de días de vacaciones'
    
    employee_ids = fields.Many2many('hr.employee', string='Empleados')
    adjustment_days = fields.Float('Días a ajustar', required=True)
    reason = fields.Text('Motivo del ajuste', required=True)
    
    def action_apply_adjustment(self):
        self.ensure_one()
        if not self.employee_ids:
            raise ValidationError(_("Debe seleccionar al menos un empleado."))
        
        for employee in self.employee_ids:
            employee.write({
                'vacation_days_available': employee.vacation_days_available + self.adjustment_days
            })
        
        return {'type': 'ir.actions.act_window_close'}