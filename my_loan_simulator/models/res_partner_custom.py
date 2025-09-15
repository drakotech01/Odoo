from odoo import models, fields, api

class ResPartnerCustom(models.Model):    
    _inherit = 'res.partner'
    _description = 'Clientes de Crédito'

    #is_loan_client = fields.Boolean(string='Es Cliente de Crédito', default=False, tracking=True)    
    custom_code = fields.Char(string='Código Interno', required=True, tracking=True)
    #partner_id = fields.Many2one('res.partner', string='Cliente', ondelete='cascade')
    #loan_ids = fields.One2many('loan.simulator', 'partner_id', string='Créditos Asociados')