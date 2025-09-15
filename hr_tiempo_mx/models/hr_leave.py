from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date

class HrLeave(models.Model):
    _inherit = 'hr.leave'
    
    # Campos adicionales
    rejection_reason = fields.Text('Motivo de Rechazo')
    is_birthday_leave = fields.Boolean(compute='_compute_is_birthday_leave', store=True)
    original_available_days = fields.Float('Días disponibles al momento de solicitud', readonly=True)
    
    @api.depends('holiday_status_id')
    def _compute_is_birthday_leave(self):
        for leave in self:
            leave.is_birthday_leave = leave.holiday_status_id.leave_category == 'birthday'
    
    @api.constrains('request_date_from', 'request_date_to', 'employee_id', 'holiday_status_id')
    def _validate_leave_dates(self):
        """Validaciones personalizadas por tipo de permiso"""
        for leave in self:
            if leave.holiday_status_id.leave_category == 'birthday':
                self._validate_birthday_leave(leave)
            elif leave.holiday_status_id.leave_category == 'vacation':
                self._validate_vacation_leave(leave)
    
    def _validate_birthday_leave(self, leave):
        """Validar que el permiso de cumpleaños sea en el mes correcto"""
        employee = leave.employee_id
        if not employee.birthday:
            raise ValidationError(_("El empleado no tiene fecha de nacimiento registrada."))
        
        birthday_month = employee.birthday.month
        leave_month = leave.request_date_from.month
        
        if birthday_month != leave_month:
            raise ValidationError(_("El permiso de cumpleaños solo puede ser tomado en el mes de nacimiento."))
        
        # Validar que no haya solicitado ya un día de cumpleaños este año
        existing_leaves = self.search([
            ('employee_id', '=', employee.id),
            ('holiday_status_id.leave_category', '=', 'birthday'),
            ('request_date_from', '>=', date(date.today().year, 1, 1)),
            ('state', 'in', ['validate', 'validate1']),
            ('id', '!=', leave.id),
        ])
        
        if existing_leaves:
            raise ValidationError(_("Ya has solicitado un permiso de cumpleaños este año."))
    
    def _validate_vacation_leave(self, leave):
        """Validar que tenga días de vacaciones disponibles"""
        available_days = leave.employee_id.vacation_days_available
        requested_days = (leave.request_date_to - leave.request_date_from).days + 1
        
        if requested_days > available_days:
            raise ValidationError(_("No tienes suficientes días de vacaciones disponibles. Días disponibles: %s") % available_days)
    
    def action_approve(self):
        """Extender la aprobación para actualizar días disponibles"""
        res = super(HrLeave, self).action_approve()
        
        for leave in self:
            if leave.holiday_status_id.leave_category == 'vacation':
                requested_days = (leave.request_date_to - leave.request_date_from).days + 1
                leave.employee_id.write({
                    'vacation_days_available': leave.employee_id.vacation_days_available - requested_days
                })
        
        return res
    
    def action_refuse(self):
        """Sobreescribir el rechazo para requerir motivo"""
        if not self.env.context.get('skip_rejection_reason'):
            if not all(leave.rejection_reason for leave in self):
                raise ValidationError(_("Debe proporcionar un motivo de rechazo para cada solicitud."))
        
        return super(HrLeave, self).action_refuse()