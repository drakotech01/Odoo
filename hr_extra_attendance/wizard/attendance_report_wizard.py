# ===========================
# IMPORTACIONES NECESARIAS
# ===========================
from odoo import models, fields
from datetime import datetime

# ===========================
# DEFINICIÓN DEL WIZARD
# ===========================
class AttendanceReportWizard(models.TransientModel):
    """
    Modelo transitorio (wizard) que permite al usuario seleccionar filtros
    personalizados para generar un reporte XLSX de asistencias.
    """
    _name = 'attendance.report.wizard'
    _description = 'Asistente para Reporte de Asistencias'

    # === CAMPOS PARA FILTRO BÁSICO ===

    date_from = fields.Date(string='Desde')  # Fecha inicial del rango
    date_to = fields.Date(string='Hasta')    # Fecha final del rango

    department_id = fields.Many2one(
        'hr.department',
        string='Departamento'
    )

    employee_id = fields.Many2one(
        'hr.employee',
        string='Empleado'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Empresa'
    )

    status = fields.Selection([
        ('solicitado', 'Solicitado'),
        ('autorizado', 'Autorizado'),
        ('rechazado', 'Rechazado')
    ], string='Estado')

    # === FILTRO POR RETARDO ===
    is_late = fields.Selection([
        ('yes', 'Sí'),
        ('no', 'No')
    ], string="¿Retardo?")

    # === FILTRO POR RANGO DE HORAS ===
    hour_min = fields.Float(
        string="Hora mínima (HH.MM)",
        help="Ejemplo: 9.5 representa 9:30 AM"
    )

    hour_max = fields.Float(
        string="Hora máxima (HH.MM)",
        help="Ejemplo: 10.25 representa 10:15 AM"
    )

    # === FILTRO POR TIPO DE DÍA (LABORAL / FIN DE SEMANA) ===
    day_type = fields.Selection([
        ('laboral', 'Día Laboral'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo')
    ], string="Tipo de día")

    # ===========================
    # MÉTODO PRINCIPAL: GENERAR REPORTE
    # ===========================
    def generate_report(self):
        """
        Este método se ejecuta al hacer clic en "Generar Reporte".
        Aplica los filtros seleccionados y retorna la acción del reporte XLSX.
        """
        domain = []  # Lista de filtros dinámicos

        # Filtrado por fecha
        if self.date_from:
            domain.append(('check_in', '>=', self.date_from))
        if self.date_to:
            domain.append(('check_in', '<=', self.date_to))

        # Filtro por departamento, empleado y empresa
        if self.department_id:
            domain.append(('department_id', '=', self.department_id.id))
        if self.employee_id:
            domain.append(('employee_id', '=', self.employee_id.id))
        if self.company_id:
            domain.append(('company_id', '=', self.company_id.id))

        # Filtro por estado de autorización del registro
        if self.status:
            domain.append(('status', '=', self.status))

        # Filtro por campo booleano de retardo
        if self.is_late == 'yes':
            domain.append(('is_late', '=', True))
        elif self.is_late == 'no':
            domain.append(('is_late', '=', False))

        # Se ejecuta la búsqueda de asistencias con los dominios base
        attendances = self.env['hr.attendance'].search(domain)

        # Filtrado adicional en Python para hora
        if self.hour_min or self.hour_max:
            attendances = attendances.filtered(
                lambda a: a.check_in and self._filter_by_hour(a.check_in)
            )

        # Filtrado adicional por tipo de día (laboral, sábado, domingo)
        if self.day_type:
            attendances = attendances.filtered(
                lambda a: self._filter_by_day_type(a.check_in)
            )

        # Devuelve la acción de impresión XLSX con los registros filtrados
        return self.env.ref(
            'hr_extra_attendance.report_attendance_xlsx'
        ).report_action(attendances)

    # ===========================
    # FUNCIÓN AUXILIAR: FILTRO POR HORA
    # ===========================
    def _filter_by_hour(self, check_in):
        """
        Convierte la hora de check_in a formato flotante (HH.MM)
        y verifica si está entre los valores mínimo y máximo.
        """
        hour_float = check_in.hour + (check_in.minute / 60.0)

        # Comparación con valores mínimo y máximo
        if self.hour_min and hour_float < self.hour_min:
            return False
        if self.hour_max and hour_float > self.hour_max:
            return False
        return True

    # ===========================
    # FUNCIÓN AUXILIAR: FILTRO POR TIPO DE DÍA
    # ===========================
    def _filter_by_day_type(self, check_in):
        """
        Evalúa el día de la semana del check_in:
        - 0 a 4 → Lunes a Viernes (laboral)
        - 5 → Sábado
        - 6 → Domingo
        """
        weekday = check_in.weekday()
        if self.day_type == 'laboral' and weekday < 5:
            return True
        if self.day_type == 'sabado' and weekday == 5:
            return True
        if self.day_type == 'domingo' and weekday == 6:
            return True
        return False
