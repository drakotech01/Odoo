from odoo import models, fields, api
from odoo.http import request

class SpreadsheetDocument(models.Model):
    _name = 'spreadsheet.document'
    _description = 'Documento de hoja de cálculo'

    name = fields.Char(required=True, string="Nombre del documento")
    data_json = fields.Text(string="Datos JSON de celdas")
    chart_type = fields.Selection([
        ('bar', 'Barra'),
        ('line', 'Línea'),
        ('pie', 'Pastel')
    ], string="Tipo de gráfico", default='bar')
    x_axis = fields.Char(string="Eje X")
    y_axis = fields.Char(string="Eje Y")

    def action_export_json(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return {
            'type': 'ir.actions.act_url',
            'url': f'{base_url}/spreadsheet/export/{self.id}',
            'target': 'new',
        }
