from odoo import models, fields, api
from datetime import timedelta

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def close_inactive_sessions(self):
        """Cierra sesiones de usuarios inactivas"""
        config = self.env['ir.config_parameter'].sudo()
        inactivity_hours = float(config.get_param('session.inactivity.hours', 8))
        
        inactive_since = fields.Datetime.now() - timedelta(hours=inactivity_hours)
        
        # Usar el modelo correcto con sudo()
        sessions = self.env['bus.presence'].sudo().search([
            ('last_presence', '<', inactive_since),
            ('status', '=', 'online')
        ])
        
        # Forzar cierre de sesión
        inactive_users = sessions.mapped('user_id')
        inactive_users.write({'access_token': False})
        
        return True