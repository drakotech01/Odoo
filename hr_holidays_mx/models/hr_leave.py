from odoo import models, fields, api
from datetime import date

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    tipo_permiso = fields.Selection([
        ('vacaciones', 'Vacaciones'),
        ('cumpleaños', 'Cumpleaños'),
        ('paternidad', 'Paternidad'),
        ('maternidad', 'Maternidad'),
        ('permiso_goce', 'Permiso con goce'),
        ('permiso_sin_goce', 'Permiso sin goce'),
        ('feriado', 'Feriado'),
    ], string='Tipo de Permiso', required=True)

    aprobado_por = fields.Many2one('hr.employee', string='Aprobado por')
    motivo = fields.Text(string='Motivo')

    @api.onchange('tipo_permiso')
    def _onchange_tipo_permiso(self):
        if self.tipo_permiso == 'cumpleaños':
            self.request_date_from = self.employee_id.birthday.replace(year=date.today().year)
            self.request_date_to = self.request_date_from

    @api.model
    def create(self, vals):
        res = super().create(vals)
        # lógica para descontar automáticamente días, validar etc.
        return res


    birthday_location_id = fields.Many2one('hr.leave.allocation', string='Locación de Cumpleaños')
    vacation_location_id = fields.Many2one('hr.leave.allocation', string='Locación de Vacaciones')

    @api.model
    def create(self, vals):
        if 'employee_id' in vals:
            employee = self.env['hr.employee'].browse(vals['employee_id'])
            # Supón que aquí defines la forma de obtener la locación por defecto para el empleado
            default_vac_location = self.env['hr.leave.location'].search([('name', '=', 'Vacaciones Generales')], limit=1)
            default_birthday_location = self.env['hr.leave.location'].search([('name', '=', 'Cumpleaños Oficina Principal')], limit=1)
            
            vals['vacation_location_id'] = default_vac_location.id if default_vac_location else False
            vals['birthday_location_id'] = default_birthday_location.id if default_birthday_location else False

        return super().create(vals)
