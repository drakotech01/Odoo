# Importación de librerías esenciales de Odoo
import requests
import logging
from odoo import models, fields, api
from datetime import datetime, timedelta
from pytz import timezone
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


_logger = logging.getLogger(__name__)

OPENCAGE_API_KEY = '1b95a7dc8d9e4e74a1b6c450d1879abc' # Clave de API para OpenCage Geocoding

# Extendemos el modelo existente 'hr.attendance' usando herencia.
# Esto nos permite agregar nuevos campos y lógica sin modificar directamente el core.
class HrAttendanceExtended(models.Model):
    _inherit = 'hr.attendance'  # Indicamos que heredamos del modelo original de asistencias.

    # =========================== Bloque para ontener la ubicación del empleado ===========================
    check_in_address = fields.Char(string="Dirección Check-In",  store=True)
    check_out_address = fields.Char(string="Dirección Check-Out", store=True)
    
    def _get_address_from_opencage(self, lat, lon):
        try:
            url = url = f'https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={OPENCAGE_API_KEY}'
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    return data['results'][0]['formatted']
        except Exception as e:
            _logger.warning(f"Error al obtener dirección: {e}")
        return ""
    
    @api.model
    def create(self, vals):
        if vals.get('in_latitude') and vals.get('in_longitude'):
            vals['check_in_address'] = self._get_address_from_opencage(
                vals['in_latitude'], vals['in_longitude']
            )
        return super().create(vals)

    def write(self, vals):
        for rec in self:
            if vals.get('out_latitude') and vals.get('out_longitude'):
                vals['check_out_address'] = self._get_address_from_opencage(
                    vals['out_latitude'], vals['out_longitude']
                )
        return super().write(vals)
    
    
    # =========================== fin Bloque para ontener la ubicación del empleado ===========================


    # Limitar la edicion del formulario cuando el registro fue diferente de modeo Manual
    registro_manual = fields.Boolean(string="Registro Manual", default=False)

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

