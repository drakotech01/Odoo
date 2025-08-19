from odoo import api, models
from datetime import datetime

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    @api.model
    def get_timer_info(self):
        """ Devuelve el tiempo objetivo (según horario) y el tiempo trabajado actual """
        employee = self.env.user.employee_id
        if not employee:
            return {"target_seconds": 0, "worked_seconds": 0}

        # Tiempo objetivo (horas del calendario)
        calendar = employee.resource_calendar_id
        target_hours = calendar.hours_per_day if calendar else 8
        target_seconds = int(target_hours * 3600)

        # Tiempo trabajado en registro activo
        worked_seconds = 0
        active_attendance = self.search([
            ('employee_id', '=', employee.id),
            ('check_out', '=', False)
        ], limit=1)
        if active_attendance:
            delta = datetime.now() - active_attendance.check_in
            worked_seconds = int(delta.total_seconds())

            # Restar pausas si el módulo las maneja
            if hasattr(active_attendance, 'pause_ids'):
                for pause in active_attendance.pause_ids:
                    if pause.end_time:
                        worked_seconds -= int((pause.end_time - pause.start_time).total_seconds())

        return {
            "target_seconds": target_seconds,
            "worked_seconds": worked_seconds
        }
