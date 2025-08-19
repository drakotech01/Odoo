# models/hr_attendance.py
from odoo import models, fields, api, _
from odoo.exceptions import AccessError, ValidationError, UserError

class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    # Dejar el campo de check_in como un campo de fecha y hora vacio - forzar la capturar
    check_in = fields.Datetime(string="Check In", default=None)

    # ******************************************************************************#
    # Campo para controlar si el formulario es de solo lectura
    is_readonly = fields.Boolean(
        compute="_compute_is_readonly",
        string="Solo lectura",
        store=False,  # No necesitamos almacenar esto en la base de datos, se calcula al vuelo.
    )

    @api.depends("in_mode")
    def _compute_is_readonly(self):
        for record in self:
            record.is_readonly = record.in_mode != "manual"

    # ******************************************************************************#
    # Boton de apronbacion
    def action_approve_overtime(self):
        self.write({'overtime_status': 'approved'})
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Registro de asistencia aprobado',
                'type': 'rainbow_man',
            }
        }
    
    def action_refuse_overtime(self):
        self.write({'overtime_status': 'refused'})
        return True

    # ******************************************************************************#

    # Campo para controlar el estado de las horas extras
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("in_mode") == "manual":
                vals["overtime_status"] = "to_approve"
        return super().create(vals_list)

    # Validar cambios de estado para registros manuales
    # ******************************************************************************#
    def write(self, vals):
            if 'overtime_status' in vals:
                for record in self:
                    if record.in_mode == 'manual':
                        # Validar si ya fue aprobado/rechazado
                        if record.overtime_status in ('approved', 'refused'):
                            raise UserError(_("No puede cambiar el estado de un registro ya aprobado/rechazado"))
            return super().write(vals)

    def action_approve_attendance(self):
        for record in self:
            if record.in_mode == 'manual' and record.overtime_status == 'to_approve':
                record.overtime_status = 'approved'
            else:
                raise UserError(_("Solo puede aprobar registros manuales en estado 'Por Aprobar'"))

    def action_reject_attendance(self):
        for record in self:
            if record.in_mode == 'manual' and record.overtime_status == 'to_approve':
                record.overtime_status = 'refused'
            else:
                raise UserError(_("Solo puede rechazar registros manuales en estado 'Por Aprobar'"))



    # ******************************************************************************#
