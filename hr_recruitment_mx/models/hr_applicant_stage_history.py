from odoo import models, fields, api
from datetime import datetime

class HrApplicantStageHistory(models.Model):
    _name = 'hr.applicant.stage.history'
    _description = 'Historial de etapas por candidato'
    _order = 'change_date desc'

    applicant_id = fields.Many2one('hr.applicant', string="Candidato", required=True, ondelete="cascade")
    stage_id = fields.Many2one('hr.recruitment.stage', string="Etapa", required=True)
    change_date = fields.Datetime(string="Fecha de entrada", default=fields.Datetime.now)
    days_in_stage = fields.Float(string="Días en la etapa anterior", compute='_compute_days_in_stage', store=True)

    @api.depends('change_date', 'applicant_id')
    def _compute_days_in_stage(self):
        for record in self:
            # Buscar la entrada anterior
            previous = self.env['hr.applicant.stage.history'].search([
                ('applicant_id', '=', record.applicant_id.id),
                ('id', '<', record.id)
            ], order='id desc', limit=1)

            if previous:
                delta = record.change_date - previous.change_date
                record.days_in_stage = round(delta.total_seconds() / 86400.0, 2)  # convertir a días
            else:
                record.days_in_stage = 0.0
