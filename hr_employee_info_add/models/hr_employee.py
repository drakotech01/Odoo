from odoo import models, fields, api
from datetime import date

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    name_mx = fields.Char(string='Nombre', required=True)
    ap_pat_mx = fields.Char(string='Apellido Paterno', required=True)
    ap_mat_mx = fields.Char(string='Apellido Materno')
    nombre_completo_mx = fields.Char(string='Nombre Completo MX', compute='_compute_nombre_completo', store=True)
    fecha_ingreso = fields.Date(string='Fecha de Ingreso', compute='_compute_fecha_ingreso', store=True)
    antiguedad_anos = fields.Integer(string='Años de Antigüedad', compute='_compute_antiguedad', store=True)
    dias_vacaciones_disponibles = fields.Integer(string='Días de Vacaciones Disponibles', compute='_compute_vacaciones', store=True)

    @api.model
    def create(self, vals):
        nombre = vals.get('name_mx', '')
        ap_pat = vals.get('ap_pat_mx', '')
        ap_mat = vals.get('ap_mat_mx', '')
        partes = list(filter(None, [nombre, ap_pat, ap_mat]))
        vals['name'] = ' '.join(partes)
        return super(HrEmployee, self).create(vals)

    def write(self, vals):
        for rec in self:
            nombre = vals.get('name_mx', rec.name_mx)
            ap_pat = vals.get('ap_pat_mx', rec.ap_pat_mx)
            ap_mat = vals.get('ap_mat_mx', rec.ap_mat_mx)
            partes = list(filter(None, [nombre, ap_pat, ap_mat]))
            vals['name'] = ' '.join(partes)
        return super(HrEmployee, self).write(vals)

    @api.depends('name_mx', 'ap_pat_mx', 'ap_mat_mx')
    def _compute_nombre_completo(self):
        for rec in self:
            partes = filter(None, [rec.name_mx, rec.ap_pat_mx, rec.ap_mat_mx])
            nombre_completo = ' '.join(partes)
            rec.nombre_completo_mx = nombre_completo
            #rec.name = nombre_completo  # Esto actualiza el campo principal 'name'

    @api.depends('contract_id.date_start')
    def _compute_fecha_ingreso(self):
        for rec in self:
            rec.fecha_ingreso = rec.contract_id.date_start if rec.contract_id and rec.contract_id.date_start else False

    @api.depends('fecha_ingreso')
    def _compute_antiguedad(self):
        for rec in self:
            if rec.fecha_ingreso:
                today = date.today()
                rec.antiguedad_anos = today.year - rec.fecha_ingreso.year - ((today.month, today.day) < (rec.fecha_ingreso.month, rec.fecha_ingreso.day))
            else:
                rec.antiguedad_anos = 0

    @api.depends('antiguedad_anos')
    def _compute_vacaciones(self):
        for rec in self:
            años = rec.antiguedad_anos
            if años <= 0:
                rec.dias_vacaciones_disponibles = 0
            elif años == 1:
                rec.dias_vacaciones_disponibles = 12
            elif años == 2:
                rec.dias_vacaciones_disponibles = 14
            elif años == 3:
                rec.dias_vacaciones_disponibles = 16
            elif años == 4:
                rec.dias_vacaciones_disponibles = 18
            elif años == 5:
                rec.dias_vacaciones_disponibles = 20
            elif años >= 6:
                extra = ((años - 6) // 5 + 1) * 2
                rec.dias_vacaciones_disponibles = 20 + extra
