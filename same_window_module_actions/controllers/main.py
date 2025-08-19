from odoo import http
from odoo.http import request

class ModuleActionsController(http.Controller):
    @http.route('/module/action/override', type='json', auth='user')
    def override_module_action(self, action, module_id):
        """Endpoint personalizado para acciones de módulo"""
        module = request.env['ir.module.module'].browse(module_id)
        
        try:
            if action == 'install':
                result = module.button_immediate_install()
            elif action == 'upgrade':
                result = module.button_immediate_upgrade()
            elif action == 'uninstall':
                result = module.button_immediate_uninstall()
            else:
                return {'error': 'Acción no válida'}
            
            # Forzar retorno sin acción de redirección
            return {'success': True, 'module_state': module.state}
        except Exception as e:
            return {'error': str(e)}