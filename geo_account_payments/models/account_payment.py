# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    # Campos para almacenar la ubicación. No tienen valor por defecto,
    # por lo que estarán vacíos al crear un pago.
    latitude = fields.Float(string="Latitud", digits=(16, 8))
    longitude = fields.Float(string="Longitud", digits=(16, 8))


    def update_coordinates(self, lat, lon):
        self.write({
            'latitude': lat,
            'longitude': lon,
        })
        # Llamar a action_post() para publicar el pago
        return super().action_post()
    