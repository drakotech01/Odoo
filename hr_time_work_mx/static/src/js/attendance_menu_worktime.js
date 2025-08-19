/** @odoo-module **/

import { ActivityMenu } from "@hr_attendance/components/attendance_menu/attendance_menu";
import { registry } from "@web/core/registry";
import { useState, onMounted, onWillUnmount } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { DateTime } from "luxon";


export class AttendanceMenuWorkTime extends ActivityMenu {
    setup() {
        super.setup();

        this.state = useState({
            ...this.state,
            worked: null,
            percentage: null,
        });

        this.workdayHours = 8;
        this.timer = null;

        onMounted(async () => {
            await this._loadEmployeeData();
        });

        onWillUnmount(() => {
            this._stopWorkTimer();
        });
    }

    async _loadEmployeeData() {
        const result = await rpc("/hr_attendance/attendance_user_data");
        this.employee = result;

        if (this.employee?.id) {
            this.state.checkedIn = this.employee.attendance_state === "checked_in";
            if (this.state.checkedIn && this.employee?.last_check_in) {
                this._startWorkTimer(this.employee.last_check_in);
            } else {
                this._stopWorkTimer();
            }
        }
    }

    _handleAttendanceState() {
        super._handleAttendanceState();
        if (this.state.checkedIn && this.employee?.last_check_in) {
            this._startWorkTimer(this.employee.last_check_in);
        } else {
            this._stopWorkTimer();
        }
    }

    _parseLocalDatetime(datetimeStr) {
        if (!datetimeStr) return null;
        // Se asume que datetimeStr viene en formato UTC "YYYY-MM-DD HH:mm:ss"
        const dt = DateTime.fromFormat(datetimeStr, "yyyy-MM-dd HH:mm:ss", { zone: 'utc' });
        if (!dt.isValid) {
            console.error("Fecha inválida:", datetimeStr);
            return null;
        }
        // Convertir a local y devolver JS Date
        return dt.setZone(DateTime.local().zoneName).toJSDate();
    }

    _startWorkTimer(startTimeStr) {
    this.attendanceStart = this._parseLocalDatetime(startTimeStr);
    console.log('Attendance Start:', this.attendanceStart, 'Now:', new Date());
    if (!this.attendanceStart) return;

    this._stopWorkTimer();
    this._updateWorkedTime();
    this.timer = setInterval(() => this._updateWorkedTime(), 1000);
}

    _stopWorkTimer() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
        this.state.worked = null;
        this.state.percentage = null;
    }

    _updateWorkedTime() {
        if (!this.attendanceStart) return;
    
        const now = new Date();
        const diffMs = Math.max(0, now - this.attendanceStart);
        const diffSec = Math.floor(diffMs / 1000);
    
        const hours = Math.floor(diffSec / 3600);
        const minutes = Math.floor((diffSec % 3600) / 60);
        const seconds = diffSec % 60;
    
        // Crear nuevas cadenas para forzar reactividad
        this.state.worked = `${hours.toString().padStart(2, "0")}:` +
                            `${minutes.toString().padStart(2, "0")}:` +
                            `${seconds.toString().padStart(2, "0")}`;
    
        this.state.percentage = (Math.min(100, (diffSec / (this.workdayHours * 3600)) * 100))
                               .toFixed(1);
    }
}

AttendanceMenuWorkTime.template = "hr_time_work_mx.AttendanceMenuWorkTime";

// Reemplaza el systray original
registry.category("systray").add("hr_attendance_attendance", {
    Component: AttendanceMenuWorkTime,
});
