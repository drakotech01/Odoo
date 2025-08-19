# Importación de librerías esenciales de Odoo
from odoo import models, fields, api
from datetime import datetime, timedelta
#from pytz import timezone
from odoo.exceptions import UserError

# Extendemos el modelo existente 'hr.attendance' usando herencia.
# Esto nos permite agregar nuevos campos y lógica sin modificar directamente el core.
class HrAttendanceExtended(models.Model):
    _inherit = 'hr.attendance'  # Indicamos que heredamos del modelo original de asistencias.


    # Limitar la edicion del formulario cuando el registro fue diferente de modeo Manual
    #registro_manual = fields.Boolean(string="Registro Manual", default=False)

    # ===========================
    # BOTONES Y ESTAUS HEADER Y WIDGET
    # ===========================

    manage_ot = fields.Boolean(
        string="Gestionar Registro Manual",
        compute="_compute_manage_ot",  # Método que calcula si se debe mostrar el botón
        store=False,
    )

    @api.depends('overtime_status')
    def _compute_manage_ot(self):
        """
        Determina si se debe mostrar el botón de gestión de registro manual.
        Solo se muestra si el estado del registro es 'Por Aprobar'.
        """
        for record in self:
            # El botón solo se muestra si el estado es 'to_approve'
            record.manage_ot = record.overtime_status == 'to_approve'
    
    def action_approve_overtime(self):
        self.ensure_one()
        # Se actualiza la condición para usar 'to_approve'
        if self.overtime_status == 'to_approve':
            self.overtime_status = 'approved'
            # Puedes añadir un mensaje al chatter o un log si es necesario
            self.message_post(body=("Overtime has been approved."))
        else:
            raise UserError(("Overtime can only be approved if its status is 'Por Aprobar'."))
    
    def action_reject_overtime(self):
        self.ensure_one()
        # Se actualiza la condición para usar 'to_approve' y el estado final a 'refused'
        if self.overtime_status == 'to_approve':
            self.overtime_status = 'refused'
            # Puedes añadir un mensaje al chatter o un log si es necesario
            self.message_post(body=("Overtime has been rejected."))
        else:
            raise UserError(("Overtime can only be rejected if its status is 'Por Aprobar'."))

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

    ap_mat_mx = fields.Char(
        string="Apellido Materno",
        related='employee_id.ap_mat_mx',  # Campo de apellido materno relacionado
        store=True, readonly=True
    )

    # Campo combinado de apellidos que concatena paterno y materno.    
    ap_completos = fields.Char(string="Apellidos", compute='_compute_apellidos', store=True)

    @api.depends('ap_pat_mx', 'ap_mat_mx')
    def _compute_apellidos(self):
        """
        Concatena apellido paterno y materno con un espacio.
        """
        for rec in self:
            ap = rec.ap_pat_mx or ''
            am = rec.ap_mat_mx or ''
            rec.ap_completos = f"{ap} {am}".strip()


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
    overtime_status = fields.Selection([
        ('to_approve', 'Por Aprobar'),
        ('approved', 'Aprobado'),
        ('refused', 'Rechazado'),
    ], string="Estado", default='to_approve', tracking=True, readonly=True)

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

    def action_approve(self):
        """
        Método invocado al presionar el botón 'Autorizar'.
        Cambia el estado del registro a 'autorizado'.
        """
        for rec in self:
             rec.overtime_status = 'approved'

    def action_refuse(self):
        """
        Método invocado al presionar el botón 'Rechazar'.
        Cambia el estado del registro a 'rechazado'.
        Se espera que el usuario escriba un motivo de rechazo.
        """
        for rec in self:
            rec.overtime_status = 'refused'

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

    # ===========================
    # CAMPOS DERIVADOS DE CHECK_OUT
    # ===========================

    # Campo para mostrar solo la fecha del registro de salida
    check_out_date = fields.Date(
            string="Fecha de Salida",
            compute="_compute_checkout_date_time",
            store=True
        )

    # Campo para mostrar solo la hora del registro
    check_out_time = fields.Char(
            string="Hora de Salida",
            compute="_compute_checkout_date_time",
            store=True
        )

    @api.depends('check_out')
    def _compute_checkout_date_time(self):
        """
        Separa el campo datetime 'check_out' en dos campos:
        - Fecha (YYYY-MM-DD)
        - Hora (HH:MM)
        Esto mejora la visualización y reporte.
        """
        for rec in self:
            if rec.check_out:
                rec.check_out_date = rec.check_out.date()  # Extraemos solo la fecha
                rec.check_out_time = rec.check_out.strftime('%H:%M')  # Extraemos la hora en formato HH:MM
            else:
                rec.check_out_date = False
                rec.check_out_time = False


    
