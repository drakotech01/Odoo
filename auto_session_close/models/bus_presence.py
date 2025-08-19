from odoo import models, fields

class BusPresence(models.Model):
    _inherit = 'bus.presence'

    # Añadir campos adicionales si es necesario
    # o simplemente heredar para asegurar la carga del modelo