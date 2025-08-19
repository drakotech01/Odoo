from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    @api.model
    def get_current_employee_id(self):
        """Obtener ID del empleado actual"""
        employee = self.env.user.employee_id
        return employee.id if employee else None
    
    @api.model
    def get_current_break_status(self, employee_id=None):
        """Obtener estado actual de pausas para un empleado"""
        if not employee_id:
            employee = self.env.user.employee_id
        else:
            employee = self.browse(employee_id)
        
        if not employee:
            return {'on_break': False, 'break_start_time': None}
        
        # Buscar asistencia activa
        attendance = self.env['hr.attendance'].search([
            ('employee_id', '=', employee.id),
            ('check_out', '=', False)
        ], limit=1)
        
        if not attendance:
            return {'on_break': False, 'break_start_time': None}
        
        # Buscar pausa activa
        active_break = self.env['hr.attendance.break'].search([
            ('attendance_id', '=', attendance.id),
            ('pause_start', '!=', False),
            ('pause_end', '=', False)
        ], limit=1)
        
        return {
            'on_break': bool(active_break),
            'break_start_time': active_break.pause_start.isoformat() if active_break else None,
            'attendance_id': attendance.id
        }