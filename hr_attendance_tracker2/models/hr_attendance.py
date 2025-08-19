from odoo import api, fields, models
from datetime import datetime

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    
    pause_ids = fields.One2many(
        'hr.attendance.pause', 
        'attendance_id', 
        string='Pausas'
    )
    is_paused = fields.Boolean(string='¿En Pausa?', default=False)

    def action_start_pause(self):
        for rec in self:
            rec.env['hr.attendance.pause'].create({
                'attendance_id': rec.id,
                'start_pause': fields.Datetime.now(),
            })
            rec.is_paused = True

    def action_end_pause(self):
        for rec in self:
            pause = rec.pause_ids.filtered(lambda p: not p.end_pause)
            if pause:
                pause[-1].end_pause = fields.Datetime.now()
            rec.is_paused = False