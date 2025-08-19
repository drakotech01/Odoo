/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useState, onWillStart, onMounted, onWillUnmount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

const { Component } = owl;

class AttendanceTimerSystray extends Component {
    setup() {
        this.orm = useService("orm");
        this.user = useService("user");
        this.state = useState({
            checkedIn: false,
            startTime: null,
            elapsed: "00:00:00",
        });

        // Al iniciar: verificar si el usuario está checkeado
        onWillStart(async () => {
            const employee = await this.orm.call(
                "hr.employee",
                "search_read",
                [[["user_id", "=", this.user.userId]]],
                ["id"]
            );
            if (employee.length) {
                const data = await this.orm.call(
                    "hr.employee",
                    "get_attendance_state",
                    [employee[0].id]
                );
                if (data.checked_in) {
                    this.state.checkedIn = true;
                    this.state.startTime = new Date(data.check_in);
                }
            }
        });

        // Iniciar temporizador
        onMounted(() => {
            this.timer = setInterval(() => {
                if (this.state.checkedIn && this.state.startTime) {
                    const diff = new Date() - new Date(this.state.startTime);
                    this.state.elapsed = this.formatTime(diff);
                }
            }, 1000);
        });

        onWillUnmount(() => {
            clearInterval(this.timer);
        });
    }

    formatTime(ms) {
        let totalSeconds = Math.floor(ms / 1000);
        let hours = String(Math.floor(totalSeconds / 3600)).padStart(2, "0");
        let minutes = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, "0");
        let seconds = String(totalSeconds % 60).padStart(2, "0");
        return `${hours}:${minutes}:${seconds}`;
    }
}

// Usamos el template OWL que está en static/src/xml/attendance_timer_systray.xml
AttendanceTimerSystray.template = "attendance_timer_systray.SystrayItem";

// ✅ Registro correcto en systray para Odoo 18
registry.category("systray").add("attendance_timer_systray", AttendanceTimerSystray);
