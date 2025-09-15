# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging
import requests

_logger = logging.getLogger(__name__)

class GeoLocation(models.Model):
    _name = 'geo.location'
    _description = 'Registro de Geolocalización'
    _order = 'last_location_update desc'
    
    name = fields.Char(
        string='Nombre del lugar',
        required=True,
        default=lambda self: _('Nueva ubicación')
    )
    
    latitude = fields.Float(
        string='Latitud',
        digits=(16, 6),
        help='Coordenada de latitud en formato decimal'
        
    )
    
    longitude = fields.Float(
        string='Longitud',
        digits=(16, 6),
        help='Coordenada de longitud en formato decimal'        
    )
    
    last_location_update = fields.Datetime(
        string='Última actualización',
        default=fields.Datetime.now
    )
    
    user_id = fields.Many2one(
        'res.users',
        string='Usuario',
        default=lambda self: self.env.user,
        readonly=True
    )
    
    address = fields.Text(
        string='Dirección completa',
        compute='_compute_address',
        store=True
    )
    
    def get_Location(self):
        pass
    
    @api.model
    def guardar_coordenadas(self, lat, lng):
        """Guardar o actualizar la ubicación del usuario actual."""
        _logger.info(f"📍 Guardando coordenadas: lat={lat}, lng={lng}")

        new_location = self.create({
            'name': 'Ubicación de ' + self.env.user.name,
            'latitude': lat,
            'longitude': lng,
            'user_id': self.env.uid,
        })

        _logger.info("✅ Nueva ubicación creada")
        return {'status': 'created', 'latitude': lat, 'longitude': lng, 'id': new_location.id}

    @api.model
    def actualizar_coordenadas(self, record_id, lat, lng):
        record = self.browse(record_id)
        if not record.exists():
            return {'error': 'Registro no encontrado'}
        record.write({
            'latitude': lat,
            'longitude': lng,
        })
    
