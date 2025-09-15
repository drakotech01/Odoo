/** @odoo-module **/

// hr_attendance_sesametime_button/static/src/js/sesametime_attendance_patch.js
import { patch } from "@web/core/utils/patch";
import { AttendanceMenu } from "@hr_attendance/components/attendance_menu/attendance_menu";
// Este es el componente del systray para la asistencia en Odoo 18

patch(AttendanceMenu.prototype, "hr_attendance_sesametime_button_systray_patch", {
    /**
     * Esta función se ejecuta cuando el componente AttendanceMenu (del systray) se inicializa.
     * Es ideal para realizar una actualización inicial del estado del botón.
     */
    setup() {
        this._super(); // Llama al método setup original del componente base.
        this._updateButtonColorAndLabel(); // Realiza la actualización inicial del botón.
    },

    /**
     * Sobrescribe el método que se llama después de una acción de asistencia (check-in/out).
     * Esto asegura que el botón se actualice inmediatamente después de un cambio.
     */
    async _onAttendanceClick(event) {
        // Ejecuta la lógica original del click de asistencia.
        // Se asume que el método original maneja el estado de asistencia.
        await this._super(event);
        // Espera un pequeño momento para que el DOM se actualice con el nuevo estado
        // (a veces es necesario si el renderizado es asíncrono).
        await this.env.services.rpc("/web/dataset/call_kw/hr.employee/search_read", {
            model: 'hr.employee',
            method: 'search_read',
            args: [[['user_id', '=', this.env.services.user.userId]], ['attendance_state']],
            kwargs: {limit: 1},
        }).then(result => {
            if (result && result.length > 0) {
                this.employee.attendance_state = result[0].attendance_state; // Actualiza el estado local del empleado
                this._updateButtonColorAndLabel(); // Actualiza el botón con el nuevo estado.
            }
        });
    },

    /**
     * Helper para actualizar las clases CSS y el texto del botón basado
     * en el estado de asistencia del empleado.
     */
    _updateButtonColorAndLabel() {
        const button = document.querySelector('.o_sesametime_attendance_button');
        if (button) {
            // Elimina ambas clases de estado para evitar conflictos
            button.classList.remove('o_sesametime_button_check_in');
            button.classList.remove('o_sesametime_button_check_out');

            // Añade la clase correcta según el estado del empleado
            if (this.employee.attendance_state === 'checked_in') {
                button.classList.add('o_sesametime_button_check_out'); // Si ya marcó entrada, el siguiente es Salida (Rojo)
            } else {
                button.classList.add('o_sesametime_button_check_in'); // Si no marcó entrada, el siguiente es Entrada (Verde)
            }

            // También actualiza el texto visible directamente si el t-if no es suficiente reactivo
            // Aunque t-if en QWeb es reactivo, esto es una capa extra de seguridad.
            const labelSpan = button.querySelector('.o_sesametime_label_text');
            const icon = button.querySelector('.fa');
            if (labelSpan && icon) {
                if (this.employee.attendance_state === 'checked_in') {
                    labelSpan.textContent = 'Salida';
                    icon.classList.remove('fa-arrow-up');
                    icon.classList.add('fa-arrow-down');
                } else {
                    labelSpan.textContent = 'Entrada';
                    icon.classList.remove('fa-arrow-down');
                    icon.classList.add('fa-arrow-up');
                }
            }
        }
    },
});