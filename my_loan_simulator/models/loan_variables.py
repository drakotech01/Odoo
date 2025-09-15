from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_interest_rate = fields.Float(
        string='Tasa de Interés por Defecto (%)',
        config_parameter='my_loan_simulator.default_interest_rate',
        help="Esta tasa se usará como valor inicial en el simulador."
    )