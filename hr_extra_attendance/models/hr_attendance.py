# Importación de librerías esenciales de Odoo
from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import UserError

# Extendemos el modelo existente 'hr.attendance' usando herencia.
# Esto nos permite agregar nuevos campos y lógica sin modificar directamente el core.
class HrAttendanceExtended(models.Model):
    _inherit = 'hr.attendance'  # Indicamos que heredamos del modelo original de asistencias.

    # ===========================
    # CAMPOS RELACIONADOS AL EMPLEADO
    # ===========================

    # Campos relacionados para mostrar nombre y datos de empleado en la vista de asistencias.
    # Se obtienen desde el modelo hr.employee (asumiendo que los campos personalizados ya existen ahí).

    name_mx = fields.Char(
        string="Nombre(s)",
        related='employee_id.name_mx',  # Campo de empleado relacionado
        store=True, readonly=True          # Se guarda en base de datos y es solo lectura
    )

    ap_pat_mx = fields.Char(
        string="Apellido Paterno",
        related='employee_id.ap_pat_mx',  # Campo de apellido paterno relacionado
        store=True, readonly=True
    )

    ap_pat_mx = fields.Char(
        string="Apellido Materno",
        related='employee_id.ap_mat_mx',  # Campo de apellido materno relacionado
        store=True, readonly=True
    )

    job_title = fields.Char(
        string="Puesto",
        related='employee_id.job_title',   # Asumimos que este campo existe en el modelo empleado
        store=True, readonly=True
    )

    department_id = fields.Many2one(
        string="Departamento",
        related='employee_id.department_id',
        store=True, readonly=True
    )

    company_id = fields.Many2one(
        string="Empresa",
        related='employee_id.company_id',
        store=True, readonly=True
    )

    # ===========================
    # CONTROL DE PUNTUALIDAD
    # ===========================

    # Campo calculado que determina si hubo retardo o no.
    is_late = fields.Boolean(
        string="¿Retardo?",
        compute="_compute_punctuality",  # Método que lo calcula automáticamente
        store=True                       # Almacena el valor en base de datos
    )

    # ===========================
    # CONTROL DE ESTADO DEL REGISTRO
    # ===========================

    # Define el estado del registro de asistencia manual:
    # solicitado → espera revisión; autorizado → aprobado; rechazado → no aprobado.
    status = fields.Selection([
        ('solicitado', 'Solicitado'),
        ('autorizado', 'Autorizado'),
        ('rechazado', 'Rechazado')
    ], string="Estado", default='solicitado', readonly=True)

    # Campo para capturar el motivo del rechazo cuando el estado es "rechazado".
    rejection_comment = fields.Text(string="Motivo de rechazo")

    # ===========================
    # FUNCIÓN PARA CALCULAR RETARDO
    # ===========================

    @api.depends('check_in')  # Esta función se ejecuta cuando cambia el campo check_in
    def _compute_punctuality(self):
        """
        Evalúa si el empleado llegó tarde o no, considerando una hora fija de entrada
        y un margen de tolerancia configurable desde el sistema.
        """
        # Obtenemos la tolerancia desde las configuraciones del sistema. Si no existe, usamos 10 minutos por defecto.
        tolerance_minutes = int(self.env['ir.config_parameter'].sudo().get_param(
            'attendance.late_tolerance', 10))

        scheduled_hour = 9  # Hora fija de entrada (9 AM). Se puede parametrizar posteriormente.

        for record in self:
            if record.check_in:
                # Creamos un datetime del mismo día con la hora exacta de entrada esperada.
                expected = record.check_in.replace(hour=scheduled_hour, minute=0, second=0)

                # Sumamos los minutos de tolerancia al horario esperado
                tolerance_limit = expected + timedelta(minutes=tolerance_minutes)

                # Comparamos la hora real de check_in con el límite de tolerancia
                record.is_late = record.check_in > tolerance_limit

    # ===========================
    # ACCIONES PARA GESTIÓN MANUAL
    # ===========================

    #def action_approve(self):
    #   """
    #   Método invocado al presionar el botón 'Autorizar'.
    #   Cambia el estado del registro a 'autorizado'.
    #   """
    #   for rec in self:
    #       rec.status = 'autorizado'
    #
    #def action_reject(self):
    #    """
    #    Método invocado al presionar el botón 'Rechazar'.
    #    Cambia el estado del registro a 'rechazado'.
    #    Se espera que el usuario escriba un motivo de rechazo.
    #    """
    #    for rec in self:
    #        rec.status = 'rechazado'

    # ===========================
    # CAMPOS DERIVADOS DE CHECK_IN
    # ===========================

    # Campo para mostrar solo la fecha del registro
    check_in_date = fields.Date(
        string="Fecha de Entrada",
        compute="_compute_checkin_date_time",
        store=True
    )

    # Campo para mostrar solo la hora del registro
    check_in_time = fields.Char(
        string="Hora de Entrada",
        compute="_compute_checkin_date_time",
        store=True
    )

    @api.depends('check_in')
    def _compute_checkin_date_time(self):
        """
        Separa el campo datetime 'check_in' en dos campos:
        - Fecha (YYYY-MM-DD)
        - Hora (HH:MM)
        Esto mejora la visualización y reporte.
        """
        for rec in self:
            if rec.check_in:
                rec.check_in_date = rec.check_in.date()  # Extraemos solo la fecha
                rec.check_in_time = rec.check_in.strftime('%H:%M')  # Extraemos la hora en formato HH:MM
            else:
                rec.check_in_date = False
                rec.check_in_time = False

    def action_approve_overtime(self):
        """
        Bloque de Funcionalidad: Aprobar Horas Extras
        Este método cambia el 'overtime_status' a 'approved'.
        Validaciones:
        - Solo se puede aprobar si el estado actual es 'pending_approval'.
        - Se asegura que solo se procese un registro a la vez (ensure_one()).
        """
        self.ensure_one()
        if self.overtime_status == 'pending_approval':
            self.overtime_status = 'approved'
            # Puedes añadir un mensaje al chatter o un log si es necesario
            self.message_post(body= ("Overtime has been approved."))
        else:
            raise UserError( ("Overtime can only be approved if its status is 'Pending Approval'."))

    def action_reject_overtime(self):
        """
        Bloque de Funcionalidad: Rechazar Horas Extras
        Este método cambia el 'overtime_status' a 'rejected'.
        Validaciones:
        - Solo se puede rechazar si el estado actual es 'pending_approval'.
        - Se asegura que solo se procese un registro a la vez (ensure_one()).
        """
        self.ensure_one()
        if self.overtime_status == 'pending_approval':
            self.overtime_status = 'rejected'
            # Puedes añadir un mensaje al chatter o un log si es necesario
            self.message_post(body= ("Overtime has been rejected."))
        else:
            raise UserError( ("Overtime can only be rejected if its status is 'Pending Approval'."))

# Nota: Este modelo asume que los campos relacionados ya existen en el modelo 'hr.employee'.