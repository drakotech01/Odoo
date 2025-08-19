from odoo import models, fields, api


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    break_ids = fields.One2many("hr.attendance.break", "attendance_id", string="Pausas")
    total_break_time = fields.Float(
        string="Tiempo total en pausas", compute="_compute_total_break_time"
    )
    in_pause = fields.Boolean(string="En pausa", default=False)

    @api.depends("break_ids.pause_duration")
    def _compute_total_break_time(self):
        """Suma la duración de todas las pausas del registro de asistencia."""
        for record in self:
            record.total_break_time = sum(record.break_ids.mapped("pause_duration"))

    @api.model
    def toggle_employee_break(self, employee_id=None):
        """Alterna la pausa de un empleado desde JS y devuelve estado actualizado."""
        if not employee_id:
            employee = self.env.user.employee_id
        else:
            employee = self.env["hr.employee"].browse(employee_id)

        if not employee:
            return {"error": True, "message": "No se encontró información del empleado"}

        attendance = self.search(
            [("employee_id", "=", employee.id), ("check_out", "=", False)], limit=1
        )
        if not attendance:
            return {
                "error": True,
                "message": "Debes estar registrado (check-in) para tomar una pausa",
            }

        return attendance.toggle_break()

    def toggle_break(self):
        """Alterna entre iniciar y finalizar pausa para este registro de asistencia."""
        self.ensure_one()

        active_break = self.env["hr.attendance.break"].search(
            [("attendance_id", "=", self.id), ("pause_end", "=", False)], limit=1
        )
        if active_break:
            active_break.pause_end = fields.Datetime.now()
            self.in_pause = False
            message = "Pausa finalizada correctamente"
            on_break = False
            break_start_time = None
        else:
            new_break = self.env["hr.attendance.break"].create(
                {"attendance_id": self.id, "pause_start": fields.Datetime.now()}
            )
            self.in_pause = True
            message = "Pausa iniciada correctamente"
            on_break = True
            break_start_time = new_break.pause_start.isoformat()

        return {
            "error": False,
            "message": message,
            "on_break": on_break,
            "break_start_time": break_start_time,
            "attendance_id": self.id,
        }

    @api.model
    def get_active_break(self, employee_id):
        """Retorna la pausa activa del empleado actual, si existe."""
            # Añadir validación de employee_id
        if not employee_id:
            return {"on_break": False, "break_start_time": None, "attendance_id": None}
            # Buscar el empleado
        attendance = self.search(
            [("employee_id", "=", employee_id), ("check_out", "=", False)], limit=1
        )
        if not attendance:
            return {"on_break": False, "break_start_time": None, "attendance_id": None}

        active_break = self.env["hr.attendance.break"].search(
            [("attendance_id", "=", attendance.id), ("pause_end", "=", False)], limit=1
        )
        return {
            "on_break": bool(active_break),
            "break_start_time": active_break.pause_start.isoformat() if active_break else None,
            "attendance_id": attendance.id,
        }
        """
        if active_break:
            return {
                "on_break": True,
                "break_start_time": active_break.pause_start.isoformat(),
                "attendance_id": attendance.id,
            }

        return {
            "on_break": False,
            "break_start_time": None,
            "attendance_id": attendance.id,
        }
        """
    def close_active_break_on_checkout(self):
        """Cierra cualquier pausa activa antes de hacer check-out"""
        self.ensure_one()
        active_break = self.env["hr.attendance.break"].search([
            ("attendance_id", "=", self.id),
            ("pause_end", "=", False)
            ], limit=1
        )
        if active_break:
            active_break.pause_end = fields.Datetime.now()
            self.in_pause = False
