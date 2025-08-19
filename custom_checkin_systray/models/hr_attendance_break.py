from odoo import models, fields, api

class HrAttendanceBreak(models.Model):
    _name = 'hr.attendance.break'
    _description = 'Registro de pausas de asistencia'
    _order = 'pause_start desc'

    attendance_id = fields.Many2one('hr.attendance', string='Asistencia', required=True, ondelete='cascade')
    employee_id = fields.Many2one(related='attendance_id.employee_id', store=True)
    pause_start = fields.Datetime(string='Inicio de pausa', required=True)
    pause_end = fields.Datetime(string='Fin de pausa')
    pause_duration = fields.Float(string='Duración (horas)', compute='_compute_duration', store=True)

    @api.depends('pause_start', 'pause_end')
    def _compute_duration(self):
        """Calcula la duración de la pausa en horas."""
        for record in self:
            if record.pause_start and record.pause_end:
                delta = record.pause_end - record.pause_start
                record.pause_duration = delta.total_seconds() / 3600.0
            else:
                record.pause_duration = 0.0

    def name_get(self):
        """Muestra la pausa con inicio y duración para interfaces legibles."""
        result = []
        for record in self:
            duration_str = f"{record.pause_duration:.2f}h" if record.pause_duration else "En curso"
            name = f"Pausa {record.pause_start.strftime('%H:%M')} - {duration_str}"
            result.append((record.id, name))
        return result
