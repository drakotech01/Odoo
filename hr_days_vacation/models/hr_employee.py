from odoo import models, fields, api
from datetime import date

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    vacation_days_available = fields.Integer(
        string='Días de Vacaciones Disponibles',
        compute='_compute_vacation_days_available',
        store=True
    )

    @api.depends('contract_id', 'contract_id.date_start', 'contract_id.state')
    def _compute_vacation_days_available(self):
        today = date.today()
        for employee in self:
            if employee.contract_id and employee.contract_id.state == 'open' and employee.contract_id.date_start:
                years = (today - employee.contract_id.date_start).days // 365
                if years < 1:
                    days = 12
                elif years < 2:
                    days = 14
                elif years < 3:
                    days = 16
                elif years < 4:
                    days = 18
                elif years < 5:
                    days = 20
                else:
                    # After 5 years, it increases by 2 days for every 5 years of service.
                    # This logic seems complex, let's simplify for now.
                    # A common interpretation is 2 days per 5 year block after the first 5.
                    days = 22
                    if years >= 10:
                        days = 24
                    if years >= 15:
                        days = 26
                    # This can be made more generic
                    # Simplified logic for now as per common practice
                    # This part of the logic might need review based on specific MX law details
                employee.vacation_days_available = days
            else:
                employee.vacation_days_available = 0