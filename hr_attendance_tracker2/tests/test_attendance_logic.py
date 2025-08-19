from odoo.tests.common import TransactionCase
from odoo import models, fields, api
from datetime import datetime

class TestAttendanceAdvanced(TransactionCase):

    def setUp(self):
        super().setUp()
        self.employee = self.env['hr.employee'].create({
            'name': 'Empleado Test',
        })

    def test_pause_recording(self):
        attendance = self.env['hr.attendance'].create({
            'employee_id': self.employee.id,
            'check_in': fields.Datetime.now(),
        })
        pause = self.env['hr.attendance.pause'].create({
            'attendance_id': attendance.id,
            'start_pause': fields.Datetime.now(),
            'end_pause': fields.Datetime.now(),
        })
        self.assertTrue(pause.duration >= 0)
