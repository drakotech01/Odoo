/** @odoo-module **/

import { Component, useState, onMounted, onWillUnmount, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

console.log("Systray Clock module loaded");
// Definición del componente SystrayClock
// Definición del componente SystrayClock mejorado
class SystrayClock extends Component {
    static template = "systray_clock.Clock";
    
    setup() {
        // Inicializar estado primero
        this.state = useState({ 
            time: "00:00:00", // Valor inicial
            is24HourFormat: false,
            showSeconds: true
        });
        
        // Inicializar después del estado
        this.animationFrameId = null;
        this.lastUpdateTime = 0;
        this.updateInterval = 1000;
        
        // Actualizar inmediatamente con el formato correcto
        this.updateTime();
        
        onMounted(() => {
            this.startAnimationTimer();
        });
        
        onWillUnmount(() => {
            this.stopAnimationTimer();
        });
    }
    
    getCurrentTime(is24HourFormat, showSeconds) {
        const now = new Date();
        let hours = now.getHours();
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
        
        let amPm = '';
        let displayHours = hours;
        
        if (!is24HourFormat) {
            amPm = hours >= 12 ? ' PM' : ' AM';
            displayHours = hours % 12 || 12;
        }
        
        displayHours = String(displayHours).padStart(2, '0');
        
        let timeString = `${displayHours}:${minutes}`;
        if (showSeconds) {
            timeString += `:${seconds}`;
        }
        if (!is24HourFormat) {
            timeString += amPm;
        }
        
        return timeString;
    }
    
    startAnimationTimer() {
        const updateTime = (timestamp) => {
            if (!this.lastUpdateTime) {
                this.lastUpdateTime = timestamp;
            }
            
            const elapsed = timestamp - this.lastUpdateTime;
            
            if (elapsed >= this.updateInterval) {
                this.updateTime();
                this.lastUpdateTime = timestamp;
            }
            
            if (this.animationFrameId !== null) {
                this.animationFrameId = requestAnimationFrame(updateTime);
            }
        };
        
        this.animationFrameId = requestAnimationFrame(updateTime);
    }
    
    stopAnimationTimer() {
        if (this.animationFrameId !== null) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
        }
    }
    
    updateTime() {
        try {
            this.state.time = this.getCurrentTime(
                this.state.is24HourFormat, 
                this.state.showSeconds
            );
        } catch (error) {
            console.warn('Error updating clock:', error);
        }
    }
    
    onClick() {
        this.state.is24HourFormat = !this.state.is24HourFormat;
        this.updateTime();
    }
    
    onRightClick(ev) {
        ev.preventDefault();
        this.state.showSeconds = !this.state.showSeconds;
        this.updateTime();
    }
}

// Registro del componente en el sistema de componentes de Odoo
export const systrayClock = {
    Component: SystrayClock,
};

// Asegurar que el componente esté disponible 
// Registrar el componente en el systray
// La propiedad 'Component' debe apuntar a nuestra clase SystrayClock
//Object.assign(window, { systrayClock });
registry.category("systray").add("systray_clock.Clock", { 
    Component: SystrayClock 
}, { sequence: 100 });