# -*- coding: utf-8 -*-
# my_loan_simulator/models/loan_simulator.py

from odoo import models, fields, api
from datetime import date, timedelta
from odoo.exceptions import UserError
import math

class LoanSimulator(models.Model):
    _name = 'loan.simulator'
    _description = 'Loan Simulator with Fixed Payments'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Se agrega el tracker aquí

        # 🔹 Estado para vista kanban y seguimiento
    state = fields.Selection([
        ("draft", "Borrador"),
        ("generated", "Generado"),
        ("done", "Finalizado"),
    ], string="Estado", default="draft", tracking=True)

    loan_amount = fields.Float(string='Monto del Crédito', required=True, tracking=True)
    interest_rate = fields.Float(string='Tasa de Interés Anual (%)', required=True, tracking=True)
    iva_rate = fields.Float(string='IVA (%)', default=16.0, required=True, tracking=True)
    number_of_payments = fields.Integer(string='Cantidad de Pagos', required=True, tracking=True)
    
    # Se eliminó el valor por defecto de la fecha de inicio para que el usuario la ingrese manualmente
    start_date = fields.Date(string='Fecha de Inicio del Crédito', required=True, tracking=True)
    first_payment_date = fields.Date(string='Fecha del Primer Pago', required=True, tracking=True)
    
    total_debt = fields.Float(string='Monto Total a Pagar', compute='_compute_summary', store=True)
    weekly_payment = fields.Float(string='Cuota Semanal Fija', compute='_compute_summary', store=True)
    total_interest_paid = fields.Float(string='Interés Total Pagado', compute='_compute_summary', store=True)
    total_iva_paid = fields.Float(string='IVA Total Pagado', compute='_compute_summary', store=True)

    payment_ids = fields.One2many('loan.payment.line', 'simulator_id', string='Plan de Pagos')

    @api.depends('loan_amount', 'interest_rate', 'iva_rate', 'number_of_payments', 'start_date', 'first_payment_date')
    def _compute_summary(self):
        """
        Calculates the fixed weekly payment and total interest and IVA.
        """
        for record in self:
            if not record.loan_amount or not record.interest_rate or not record.number_of_payments or record.number_of_payments <= 0 or not record.start_date or not record.first_payment_date:
                record.weekly_payment = 0.0
                record.total_interest_paid = 0.0
                record.total_iva_paid = 0.0
                record.total_debt = 0.0
                continue
            
            # Daily interest and IVA rates
            daily_interest_rate = (record.interest_rate / 100) / 360
            iva_rate = record.iva_rate / 100

            # Calculate interest for the first period based on prorated days
            days_in_first_period = (record.first_payment_date - record.start_date).days
            first_payment_interest = record.loan_amount * daily_interest_rate * days_in_first_period
            
            # Calculate interest for subsequent payments (assuming 7 days per week)
            weekly_interest = record.loan_amount * daily_interest_rate * 7

            # Calculate total interest paid over all periods
            total_interest = first_payment_interest + (record.number_of_payments - 1) * weekly_interest
            total_iva = total_interest * iva_rate
            
            # Calculate the total debt and the fixed weekly payment amount
            record.total_debt = record.loan_amount + total_interest + total_iva
            record.weekly_payment = record.total_debt / record.number_of_payments
            
            record.total_interest_paid = total_interest
            record.total_iva_paid = total_iva

    def generate_amortization_schedule(self):
        """
        Generates the amortization schedule with a fixed payment amount.
        """
        self.ensure_one()
        self.payment_ids.unlink()
        
        if not self.start_date or not self.first_payment_date:
            raise UserError('Please fill in both the start date and the first payment date.')
        
        if self.first_payment_date < self.start_date:
            raise UserError('The first payment date must be after the start date of the loan.')

        # Rates
        daily_interest_rate = (self.interest_rate / 100) / 360
        iva_rate = self.iva_rate / 100

        # Fixed weekly payment from the computed field
        fixed_payment = self.weekly_payment
        
        # Initial balances
        current_balance = self.loan_amount
        current_total_debt = self.total_debt
        current_date = self.start_date

        for i in range(1, self.number_of_payments + 1):
            
            if i == 1:
                # First payment: interest prorated by days
                days_in_period = (self.first_payment_date - current_date).days
                current_payment_date = self.first_payment_date
            else:
                # Subsequent payments: fixed interest for 7 days
                days_in_period = 7
                current_payment_date = current_date + timedelta(days=days_in_period)

            # Calculation of interest and IVA based on the initial loan amount
            interest_amount = self.loan_amount * daily_interest_rate * days_in_period
            iva_amount = interest_amount * iva_rate

            # Principal is the fixed payment minus interest and IVA
            principal_amount = fixed_payment - interest_amount - iva_amount
            
            # Final balance calculations
            final_balance = current_balance - principal_amount
            final_total_debt = current_total_debt - fixed_payment
            
            # Adjust last payment to ensure final balance is zero
            if i == self.number_of_payments:
                principal_amount = current_balance
                final_balance = 0.0
                final_total_debt = 0.0
                # Recalculate payment_amount for the last period to be precise
                payment_amount = principal_amount + interest_amount + iva_amount
            else:
                payment_amount = fixed_payment

            self.env['loan.payment.line'].create({
                'simulator_id': self.id,
                'payment_number': i,
                'payment_date': current_payment_date,
                'initial_balance': round(current_balance,2),
                'principal_amount': principal_amount,
                'interest_amount': round(interest_amount,2),
                'iva_amount': round(iva_amount,2),
                'payment_amount': payment_amount,
                'final_balance': final_balance,
                'initial_total_debt': current_total_debt,
                'final_total_debt': final_total_debt,
            })
            
            current_balance = final_balance
            current_total_debt = final_total_debt
            current_date = current_payment_date

class LoanPaymentLine(models.Model):
    _name = 'loan.payment.line'
    _description = 'Loan Payment Line'

    simulator_id = fields.Many2one('loan.simulator', string='Simulador')
    payment_number = fields.Integer(string='No. de Pago')
    payment_date = fields.Date(string='Fecha de Pago')
    initial_balance = fields.Float(string='Saldo Inicial de Capital')
    principal_amount = fields.Float(string='Capital')
    interest_amount = fields.Float(string='Interés')
    iva_amount = fields.Float(string='IVA')
    payment_amount = fields.Float(string='Cuota Total')
    final_balance = fields.Float(string='Saldo Final de Capital')
    
    # Nuevos campos para el saldo total (capital + interés + IVA)
    initial_total_debt = fields.Float(string='Saldo Inicial de Deuda Total')
    final_total_debt = fields.Float(string='Saldo Final de Deuda Total')
