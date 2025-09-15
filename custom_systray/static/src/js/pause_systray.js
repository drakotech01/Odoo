/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { useState } from "@odoo/owl";

console.log("✅ Pause Systray cargado correctamente");

patch(Object.prototype, {
    togglePause() {
        this.state.onBreak = !this.state.onBreak;
        console.log(this.state.onBreak ? "🛑 Pausa iniciada" : "▶️ Pausa terminada");
        // RPC para guardar pausa en backend
    },

    setup() {
        if (this.state && "checkedIn" in this.state && !("onBreak" in this.state)) {
            this.state.onBreak = false;
        }
    },
});