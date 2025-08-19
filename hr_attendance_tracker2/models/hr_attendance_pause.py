from odoo import models, fields, api
from datetime import timedelta

class HrAttendancePause(models.Model):
    _name = 'hr.attendance.pause'
    _description = 'Pausa de asistencia'

    attendance_id = fields.Many2one('hr.attendance', string='Asistencia', required=True)
    start_pause = fields.Datetime(string='Inicio de Pausa', required=True)
    end_pause = fields.Datetime(string='Fin de Pausa')
    duration = fields.Float(string='Duración (horas)', compute='_compute_duration', store=True)

    @api.depends('start_pause', 'end_pause')
    def _compute_duration(self):
        for rec in self:
            if rec.start_pause and rec.end_pause:
                rec.duration = (rec.end_pause - rec.start_pause).total_seconds() / 3600
            else:
                rec.duration = 0.0
