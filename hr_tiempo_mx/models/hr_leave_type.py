from odoo import models, fields, api

class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'
    
    # Tipos de permiso adicionales
    leave_category = fields.Selection([
        ('vacation', 'Vacaciones'),
        ('birthday', 'Día de Cumpleaños'),
        ('paid', 'Permiso con Goce de Sueldo'),
        ('unpaid', 'Permiso sin Goce de Sueldo'),
        ('paternity', 'Permiso de Paternidad'),
        ('maternity', 'Permiso de Maternidad'),
        ('holiday', 'Día Festivo'),
    ], string='Categoría de Permiso', default='vacation')
    
    # Configuraciones específicas por tipo
    requires_birthday_validation = fields.Boolean('Requiere validación de fecha de nacimiento')
    is_legal_leave = fields.Boolean('Es permiso legal (paternidad/maternidad)')
    max_days_per_year = fields.Integer('Días máximos por año')
    allow_carry_over = fields.Boolean('Permite acumulación')
    
    # Restricciones para días de cumpleaños
    birthday_month_only = fields.Boolean('Solo válido en mes de cumpleaños')