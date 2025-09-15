# models/attendance_cron.py
from odoo import models, fields, api
from datetime import datetime, time
import pytz
import logging

_logger = logging.getLogger(__name__)

class AttendanceCron(models.Model):
    _name = 'attendance.cron'
    _description = 'Cron para cerrar registros de asistencia'

    @api.model
    def close_previous_day_attendances(self):
        """
        Cierra los registros de asistencia de días anteriores
        Coloca la hora de cierre a las 19:00 hrs del día del registro
        """
        # Obtener la fecha actual
        current_date = fields.Date.today()
        
        # Buscar registros de asistencia que no sean del día actual y que no tengan check_out
        attendance_obj = self.env['hr.attendance']
        open_attendances = attendance_obj.search([
            ('check_in', '<', current_date),
            ('check_out', '=', False)
        ])
        
        closed_count = 0
        
        for attendance in open_attendances:
            try:
                # Obtener la fecha del check_in
                check_in_date = attendance.check_in.date()
                
                # Crear datetime para las 19:00 hrs del día del check_in
                close_time = datetime.combine(check_in_date, time(19, 0, 0))
                
                # Convertir a UTC considerando la zona horaria
                close_time_utc = self._convert_to_utc(close_time)
                
                # Actualizar el registro con el check_out (sin el campo auto_closed)
                attendance.write({
                    'check_out': close_time_utc,
                })
                
                closed_count += 1
                
            except Exception as e:
                # Registrar error pero continuar con otros registros
                _logger.error("Error al cerrar asistencia ID %s: %s", attendance.id, str(e))
                continue
        
        _logger.info("Se cerraron %s registros de asistencia de días anteriores", closed_count)
        return closed_count

    def _convert_to_utc(self, local_dt):
        """Convierte datetime local a UTC considerando la zona horaria del usuario"""
        user_tz = self.env.user.tz or 'UTC'
        try:
            local_tz = pytz.timezone(user_tz)
            # Localizar el datetime y convertir a UTC
            localized_dt = local_tz.localize(local_dt)
            utc_dt = localized_dt.astimezone(pytz.utc)
            return utc_dt.replace(tzinfo=None)
        except Exception:
            # Si hay error con la zona horaria, usar UTC
            return local_dt.replace(tzinfo=pytz.utc)