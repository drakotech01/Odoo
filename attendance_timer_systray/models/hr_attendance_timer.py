from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def get_attendance_state(self):
        """Devuelve si el empleado está actualmente checkeado y la hora de entrada"""
        self.ensure_one()
        attendance = self.env["hr.attendance"].search([
            ("employee_id", "=", self.id),
            ("check_out", "=", False)
        ], limit=1, order="check_in desc")
        if attendance:
            return {
                "checked_in": True,
                "check_in": attendance.check_in,
            }
        return {"checked_in": False, "check_in": False}
