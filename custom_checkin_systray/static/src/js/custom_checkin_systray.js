/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { ActivityMenu } from "@hr_attendance/components/attendance_menu/attendance_menu";
import { Component } from "@odoo/owl";


console.log("Pausas Button: Componente registrado");
// Guardar referencia a los métodos originales
const originalSignInOut = ActivityMenu.prototype.signInOut;
const originalDestroy = ActivityMenu.prototype.destroy;
const originalSetup = ActivityMenu.prototype.setup;

// Aplicar patch sin nombre, solo con el objeto de propiedades
patch(ActivityMenu.prototype, {
    setup() {
        // Llamada al setup original usando la referencia guardada        
            originalSetup.apply(this, arguments);
        

        Object.assign(this.state, {
            onBreak: false,
            breakStartTime: null,
            attendanceId: null,
            employeeId: null,
        });
        if (this.employee && this.employee.id) {
            this.state.onBreak = this.employee.attendance_state === "on_break";
            // Si tienes más datos de pausa en el RPC original, úsalos aquí
            // this.state.breakStartTime = this.employee.break_start_time;
            // this.state.attendanceId = this.employee.last_attendance_id;
        }
        
        
        console.log("Employee ID:", this.state.employeeId);
        console.log("Checked In:", this.state.checkedIn);
        console.log("Attendance ID:", this.state.attendanceId);
        console.log("Break Start Time:", this.state.breakStartTime);
        console.log("On Break:", this.state.onBreak);
        console.log("State:", this.state);
        console.log("functions:", this.functions);

        this.orm = this.orm || useService("orm");
        this.notification = this.notification || useService("notification");

        this.__setupBreakState();
        // Configura el polling
        this.__setupPolling();
    },

    async __setupBreakState() {
        // 1. Obtener employeeId primero
        await this._getCurrentEmployeeId();

        // 2. Actualizar estado de asistencia base
        await this._updateBaseAttendance();

        // 3. Verificar pausas activas
        await this._checkActiveBreaks();

        // 4. Configurar polling solo para actualizaciones de tiempo
        this.__setupPolling();
        console.log("Employee ID:", this.state.employeeId);
        console.log("Checked In:", this.state.checkedIn);
        console.log("On Break:", this.state.onBreak);
        console.log("Employee ID:", this.state.employeeId);
        console.log("Checked In:", this.state.checkedIn);
        console.log("Attendance ID:", this.state.attendanceId);
        console.log("Break Start Time:", this.state.breakStartTime);
        console.log("On Break:", this.state.onBreak);
        console.log("State:", this.state);
        console.log("functions:", this.functions);
    },

    async _updateBaseAttendance() {
        // Actualizar estado base usando el método original del componente
        await this.searchReadEmployee();
    },

    __setupPolling() {
        // Solo actualizar el tiempo si hay pausa activa
        if (this.timerInterval) clearInterval(this.timerInterval);
        this.timerInterval = setInterval(() => {
            if (this.state.onBreak) {
                this.render(); // Forzar actualización de UI
            }
        }, 1000);
    },

    async togglePause() {
        const employeeId = this.state.employeeId || await this._getCurrentEmployeeId();
        if (!employeeId) {
            this.notification.add(this.env._t("No se pudo obtener información del empleado"), { type: "warning" });
            return;
        }
        if (!this.state.checkedIn) {
            this.notification.add(this.env._t("Debes estar registrado para tomar una pausa"), { type: "warning" });
            return;
        }

        try {
            const result = await this.orm.call("hr.attendance", "toggle_employee_break", [employeeId]);
            if (result.error) {
                this.notification.add(result.message, { type: "warning" });
                return;
            }
            await this._checkActiveBreaks();
            await this.searchReadEmployee()
            this.notification.add(result.message, { type: "success" });
            this.__setupPolling();
        } catch (error) {
            console.error("Error al alternar pausa:", error);
            this.notification.add(
                this.env._t("Error al procesar la pausa. Intenta nuevamente."), 
                { type: "danger" }
            );
        }
    },

    async signInOut() {
        // Cerrar pausa activa si existe
        if (this.state.checkedIn && this.state.onBreak) {
            await this.orm.call("hr.attendance", "close_active_break_on_checkout", [this.state.attendanceId]);
            this.state.onBreak = false;
            this.state.breakStartTime = null;
        }

        // Llamar al método original usando referencia guardada
        return originalSignInOut.apply(this, arguments);
    },

    destroy() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
        }
        // Llamar al método original usando referencia guardada
        return originalDestroy.apply(this, arguments);
    },

    async _getCurrentEmployeeId() {
        try {
            const result = await this.orm.call("hr.employee", "get_current_employee_id", []);
            this.state.employeeId = result;
            return result;
        } catch (error) {
            console.error("Error al obtener employeeId:", error);
            return null;
        }
    },

    async _checkActiveBreaks() {
        try {
            const result = await this.orm.call("hr.attendance", "get_active_break", [this.state.employeeId]);
            this.state.onBreak = !!result.on_break;
            this.state.breakStartTime = result.break_start_time || null;
            this.state.attendanceId = result.attendance_id || null;
        } catch (error) {
            console.error("Error al verificar estado de pausas:", error);
            this.state.onBreak = false;
            this.state.breakStartTime = null;
            this.state.attendanceId = null;
        }
    },

    getCurrentBreakDuration() {
        if (!this.state.onBreak || !this.state.breakStartTime) return "00:00";

        const now = new Date();
        const breakStart = new Date(this.state.breakStartTime);
        const diff = now - breakStart;

        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

        return `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}`;
    }
});