import datetime
from odoo import api, SUPERUSER_ID

def post_install_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Actualizar el cron para que se ejecute mañana a las 23:59
    cron = env.ref('auto_session_close.ir_cron_close_checkins')
    if cron:
        now = datetime.datetime.now()
        tomorrow = now + datetime.timedelta(days=1)
        nextcall = tomorrow.replace(hour=23, minute=59, second=0, microsecond=0)
        cron.write({'nextcall': nextcall})
    
    # Configurar parámetro por defecto para inactividad
    env['ir.config_parameter'].sudo().set_param('session.inactivity.hours', 8)