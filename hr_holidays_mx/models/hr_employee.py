from odoo import models, fields, api
from datetime import date

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def _create_default_leave_allocations(self):
        """Crear asignaciones predeterminadas para vacaciones y cumpleaños"""
        allocation_model = self.env['hr.leave.allocation']
        holidays_model = self.env['hr.leave.type']

        vacation_type = holidays_model.search([('name', '=', 'Vacaciones')], limit=1)
        birthday_type = holidays_model.search([('name', '=', 'Cumpleaños')], limit=1)
        

        for employee in self:
            # Vacaciones
            if vacation_type:
                allocation_model.create({
                    'name': 'Vacaciones Iniciales',
                    'employee_id': employee.id,
                    'holiday_status_id': vacation_type.id,
                    'number_of_days': 12,
                    'allocation_type': 'regular',
                    'state': 'validate',
                    'holiday_type': 'employee',
                })

            # Cumpleaños
            if birthday_type:
                allocation_model.create({
                    'name': 'Día de Cumpleaños',
                    'employee_id': employee.id,
                    'holiday_status_id': birthday_type.id,
                    'number_of_days': 1,
                    'allocation_type': 'regular',
                    'state': 'validate',
                    'holiday_type': 'employee',
                })

    @api.model
    def create(self, vals):
        employee = super().create(vals)
        employee._create_default_leave_allocations()
        return employee

    @api.model
    def generate_allocations_for_all_employees(self):
        employees = self.search([])
        employees._create_default_leave_allocations()

    @api.model
    def button_generate_allocations(self):
        self._create_default_leave_allocations()
        return True

    @api.model
    def create(self, vals):
        empleado = super().create(vals)
        # Crear asignación de vacaciones con días permitidos por defecto
        allocation_vals = {
            'name': 'Asignación inicial de vacaciones',
            'employee_id': empleado.id,
            'holiday_status_id': self.env.ref('hr_holidays.holiday_status_cl').id,  # tipo vacaciones
            'number_of_days': 12,  # días por defecto
            'allocation_type': 'fix',
        }
        self.env['hr.leave.allocation'].create(allocation_vals)
        return empleado

    def button_actualizar_dias(self):
        for empleado in self:
            asignaciones = self.env['hr.leave.allocation'].search([('employee_id', '=', empleado.id)])
            for asignacion in asignaciones:
                dias_permitidos = 12  # o cálculo dinámico
                asignacion.write({'number_of_days': dias_permitidos})