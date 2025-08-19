# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    show_create_employee_button = fields.Boolean(compute='_compute_show_create_button', store=False,)

    @api.depends('employee_id')
    def _compute_show_create_button(self):
        for rec in self:
            rec.show_create_employee_button = not bool(rec.employee_id)

    candidate_id = fields.Many2one('hr.candidate', string="Candidato",)
    # Campos extendidos para empleados personalizados
    name_mx = fields.Char(string='Nombre(s)', required=True)
    ap_pat_mx = fields.Char(string='Apellido Paterno', required=True)
    ap_mat_mx = fields.Char(string='Apellido Materno')
    full_name_mx = fields.Char(string='Nombre Completo MX', compute='_compute_full_name', store=True)
    status_applicant = fields.Selection([
        ('cancel', 'Cancel'),
        ('aprobado', 'Aprobado'),
        ], string='Estado del Candidato', compute='_compute_status_applicant', store=True,)
    
    # Dirección extendida de empleados personalizada
    st_name_mx = fields.Char(string='Calle', required=True)
    st_num_mx = fields.Char(string='Número Exterior', required=True)
    st_num_int_mx = fields.Char(string='Número Interior')
    st_colony_mx = fields.Char(string='Colonia', required=True)
    address_mx = fields.Char(string='Dirección Principal', compute='_compute_full_address', store=True)

    # Nivel de Estudios Personalizado
    level_edu_mx = fields.Selection([
        ('primaria', 'Primaria'),
        ('secundaria', 'Secundaria'),
        ('preparatoria', 'Preparatoria'),
        ('tecnico', 'Técnico'),
        ('licenciatura', 'Licenciatura'),
        ('maestria', 'Maestría'),
        ('doctorado', 'Doctorado'),
        ('otro', 'Otro'),
    ], string='Nivel de Estudios', store=True)

    # Estado de Estudios Campo personalizado
    lvl_edu_mx = fields.Selection([
        ('titulo', 'Titulado'),
        ('egresado', 'Egresado'),
        ('cursando', 'Cursando'),
        ('trunca', 'Trunca'),
        ('pasante', 'Pasante'),        
    ], string='Estado de Estudios', store=True )

    #******Boton para cambio de etapa utilizando el boton de odoo Bloque **********       
    def write(self, vals):
        res = super(HrApplicant, self).write(vals)

        if 'kanban_state' in vals:
            for applicant in self:
                # Actualizamos solo si cambió el kanban_state
                new_state = vals.get('kanban_state')
                current_stage = applicant.stage_id

                stages = self.env['hr.recruitment.stage'].search([], order='sequence ASC')
                if not stages or current_stage.id not in stages.ids:
                    continue

                index = stages.ids.index(current_stage.id)

                # Avanzar si es 'done'
                if new_state == 'done' and index + 1 < len(stages):
                    next_stage = stages[index + 1]
                    applicant.stage_id = next_stage.id

                # Enviar a "rechazado" si es 'blocked'
                elif new_state == 'blocked':
                    rejected = self.env['hr.recruitment.stage'].search([
                        ('name', 'ilike', 'rechazado')
                    ], limit=1)
                    if rejected:
                        applicant.stage_id = rejected.id

                # Opcional: regresar a primera si es 'normal'
                elif new_state == 'normal' and index > 0:
                    first = stages[0]
                    applicant.stage_id = first.id

        return res
    
    #*****************Termina Bloque de cambio de etapa************************************#
    #************************ Asignar Full Name a Candidate.id ********************************#
    """@api.model
    def create(self, vals):
        if vals.get('name_mx') or vals.get('ap_pat_mx') or vals.get('ap_mat_mx'):
            vals['full_name_mx'] = ' '.join(filter(None, [vals.get('name_mx', ''), vals.get('ap_pat_mx', ''), vals.get('ap_mat_mx', '')]))
        return super().create(vals)

    def write(self, vals):
        for record in self:
            name = vals.get('name_mx', record.name_mx)
            pat = vals.get('ap_pat_mx', record.ap_pat_mx)
            mat = vals.get('ap_mat_mx', record.ap_mat_mx)
            vals['full_name_mx'] = ' '.join(filter(None, [name, pat, mat]))
        return super().write(vals)"""

    # Actualizar el campo en el candidato
    @api.depends('name_mx', 'ap_pat_mx', 'ap_mat_mx')
    def _compute_full_name(self):
        for rec in self:
            nombres = filter(None, [rec.name_mx, rec.ap_pat_mx, rec.ap_mat_mx])
            rec.full_name_mx = " ".join(nombres)
            

    # Asignar el nombre si viene desde 'full_name_mx'    
    @api.model
    def create(self, vals):
        # Crear el candidato automáticamente si no está definido
        if not vals.get('candidate_id') and vals.get('full_name_mx'):
            candidate = self.env['hr.candidate'].create({
                'name': vals['full_name_mx'],
            })
            vals['candidate_id'] = candidate.id

        return super().create(vals)

    def write(self, vals):
        # Si se actualiza full_name_mx, también actualizar el candidato
        res = super().write(vals)
        for record in self:
            if 'full_name_mx' in vals and record.candidate_id:
                record.partner_name = record.full_name_mx
        return res

    @api.onchange('full_name_mx')
    def _onchange_full_name_mx(self):
        if self.full_name_mx and not self.candidate_id:
            # Solo cambia visualmente, no guarda aún
            self.candidate_id = self.env['hr.candidate'].search([('partner_name', '=', self.full_name_mx)], limit=1)
    #************************ Fin de Bloque Nombre personalizado ********************************#
   
    """@api.model
    def create(self, vals):
        if vals.get('full_name_mx'):
            vals['name'] = vals['full_name_mx']  # Se usa como nombre principal del candidato            
        #return super(HrApplicant, self).create(vals)

        # Crear el registro primero para obtener el ID
        applicant = super(HrApplicant, self).create(vals)"""

    # ******** Método para rechazar el candidato (etapa final de rechazo) *******************
    def action_reject_applicant(self):
        for applicant in self:
            reject_stage = self.env['hr.recruitment.stage'].search([
                ('job_id', '=', applicant.job_id.id),
                ('name', 'ilike', 'rechazado')  # Puede ser "Rechazado" u otro similar
            ], limit=1)

            if not reject_stage:
                raise UserError(_("No hay una etapa de rechazo configurada."))

            applicant.write({
                'stage_id': reject_stage.id,
                'state': 'cancel'
            })
    #************************* Fin del Bloque **************************************
    #******************* Evitar retroceso de etapa manual **************************
    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        if self.stage_id and self.stage_id.sequence < self._origin.stage_id.sequence:
            raise UserError(_("No puedes regresar a una etapa anterior."))
    #******************* Fin del Bloque ********************************************

   #************* Crea un empleado desde el candidato y redirige a su formulario ******************   
    def action_create_employee_custom(self):        
        for applicant in self:
            if applicant.employee_id:
                raise UserError(_("Este candidato ya tiene un empleado vinculado."))

            # Construir el nombre completo personalizado
            """
            nombre = applicant.name_mx or ''
            paterno = applicant.ap_pat_mx or ''
            materno = applicant.ap_mat_mx or ''
            full_name = f"{nombre} {paterno} {materno}".strip() or "Empleado"   
            """
            # Preparar los datos del nuevo empleado
            employee_vals = {
                'name': applicant.full_name_mx,
                'name_mx': applicant.name_mx,
                'ap_pat_mx': applicant.ap_pat_mx,
                'ap_mat_mx': applicant.ap_mat_mx,
                'job_id': applicant.job_id.id if applicant.job_id else False,                 
                'department_id': applicant.department_id.id if applicant.department_id else False,
                'work_email': applicant.email_from,
                'work_phone': applicant.partner_phone,
                'st_name_mx': applicant.st_name_mx,
                'st_num_mx': applicant.st_num_mx,
                'st_num_int_mx': applicant.st_num_int_mx,
                #'birth_date': getattr(applicant, 'birth_date', False),
                #'rfc': getattr(applicant, 'rfc', ''),
                #'curp': getattr(applicant, 'curp', ''),
                'image_1920': False,  # evita el avatar
            }

            # Crear el empleado
            employee = self.env['hr.employee'].sudo().with_context(skip_avatar=True).create(employee_vals)

            # Enlazar el empleado al applicant
            applicant.employee_id = employee.id

            # Devolver acción para redirigir al formulario del nuevo empleado
            return {
                'type': 'ir.actions.act_window',
                'name': _('Empleado'),
                'view_mode': 'form',
                'res_model': 'hr.employee',
                'res_id': employee.id,
                'target': 'current',
            }
    #************ Fin del Bloque de creación de empleado personalizado ***********************

    # ************ Botón que avanza a la siguiente etapa ***********************
    
    
    
    def write(self, vals):
        # Guardar si se cambia el estado a 'done'
        trigger_advance = False
        if 'kanban_state' in vals and vals['kanban_state'] == 'done':
            trigger_advance = True

        result = super(HrApplicant, self).write(vals)

        if trigger_advance:
            for applicant in self:
                applicant.action_advance_stage()
        return result

    def action_advance_stage(self):
        for applicant in self:
            stages = self.env['hr.recruitment.stage'].search([], order='sequence ASC')
            current_index = stages.ids.index(applicant.stage_id.id)            
            if current_index + 1 < len(stages):
                    next_stage = stages[current_index + 1]
                    applicant.stage_id = next_stage.id
                    applicant.kanban_state = 'normal' # Marcar como "en progreso"


    def set_kanban_new(self):
        self.write({'kanban_state': 'normal'})

    def set_kanban_blocked(self):
        self.write({'kanban_state': 'blocked'})

    def set_kanban_done(self):
        self.write({'kanban_state': 'done'})
        # Avanza automáticamente si está en 'done'
        for applicant in self:
            applicant.action_advance_stage()

    
    #************* Ubicar la ultima etapa del candidato ****************
    
   

    @api.depends('kanban_state', 'application_status')
    def _compute_status_applicant(self):
        for rec in self:
            
            if rec.application_status == 'hired' and rec.kanban_state == 'done':
                rec.status_applicant = 'aprobado'
            elif rec.application_status == 'refused':
                rec.status_applicant == 'aprobado'
            else:
                rec.status_applicant == 'cancel'



    # Método para registrar el historial de etapas del candidato - Mejora

