/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

/**
 * Componente Systray para funcionalidad de pausar/reanudar
 */
class SystrayButtons extends Component {
    static template = "hr_attendance_tracker.SystrayButtons";
    
    setup() {
        console.log("SystrayButtons: Componente inicializado");
        
        // Usa useState para gestionar el estado de los botones
        this.state = useState({
            is_paused: false,
            is_loading: false,
        });
        
        // Inicializa los servicios de forma segura
        this.notification = null;
        this.rpc = null;
        
        // Intenta inicializar los servicios de forma diferida
        this._initializeServices();
        
        console.log("SystrayButtons: Estado inicial:", this.state);
    }

    /**
     * Inicializa los servicios de forma segura
     */
    _initializeServices() {
        try {
            // Intenta obtener los servicios
            this.notification = useService("notification");
            this.rpc = useService("rpc");
            console.log("SystrayButtons: Servicios inicializados correctamente");
        } catch (error) {
            console.warn("SystrayButtons: Error al inicializar servicios:", error);
            // Los servicios se inicializarán cuando estén disponibles
        }
    }

    /**
     * Obtiene el servicio de forma segura
     */
    _getService(serviceName) {
        try {
            if (serviceName === "notification" && !this.notification) {
                this.notification = useService("notification");
            }
            if (serviceName === "rpc" && !this.rpc) {
                this.rpc = useService("rpc");
            }
            return serviceName === "notification" ? this.notification : this.rpc;
        } catch (error) {
            console.warn(`SystrayButtons: Servicio ${serviceName} no disponible:`, error);
            return null;
        }
    }

    /**
     * Muestra una notificación de forma segura
     */
    _showNotification(message, type = 'info') {
        const notification = this._getService("notification");
        if (notification) {
            notification.add(message, { type: type });
        } else {
            console.log(`Notificación [${type}]: ${message}`);
        }
    }

    /**
     * Maneja el evento de clic del botón Pausar
     */
    async onClickPause() {
        console.log("SystrayButtons: Clic en Pausar");
        
        if (this.state.is_loading) return;
        
        try {
            this.state.is_loading = true;
            console.log("SystrayButtons: Pausando sistema...");
            
            // Obtiene el servicio RPC de forma segura
            const rpcService = this._getService("rpc");
            
            if (rpcService) {
                // Llamada RPC real cuando el servicio esté disponible
                // await rpcService.call('/web/dataset/call_kw', {
                //     model: 'hr.attendance.tracker',
                //     method: 'pause_system',
                //     args: [],
                //     kwargs: {}
                // });
                
                // Por ahora simulamos la llamada
                await new Promise(resolve => setTimeout(resolve, 1000));
            } else {
                // Simulación si el servicio no está disponible
                console.warn("SystrayButtons: Servicio RPC no disponible, usando simulación");
                await new Promise(resolve => setTimeout(resolve, 1000));
            }
            
            this.state.is_paused = true;
            this._showNotification("Sistema Pausado", 'success');
            
        } catch (error) {
            console.error("Error al pausar el sistema:", error);
            this._showNotification("Error al pausar el sistema", 'danger');
        } finally {
            this.state.is_loading = false;
        }
    }

    /**
     * Maneja el evento de clic del botón Reanudar
     */
    async onClickResume() {
        console.log("SystrayButtons: Clic en Reanudar");
        
        if (this.state.is_loading) return;
        
        try {
            this.state.is_loading = true;
            console.log("SystrayButtons: Reanudando sistema...");
            
            // Obtiene el servicio RPC de forma segura
            const rpcService = this._getService("rpc");
            
            if (rpcService) {
                // Llamada RPC real cuando el servicio esté disponible
                // await rpcService.call('/web/dataset/call_kw', {
                //     model: 'hr.attendance.tracker',
                //     method: 'resume_system',
                //     args: [],
                //     kwargs: {}
                // });
                
                // Por ahora simulamos la llamada
                await new Promise(resolve => setTimeout(resolve, 1000));
            } else {
                // Simulación si el servicio no está disponible
                console.warn("SystrayButtons: Servicio RPC no disponible, usando simulación");
                await new Promise(resolve => setTimeout(resolve, 1000));
            }
            
            this.state.is_paused = false;
            this._showNotification("Sistema Reanudado", 'success');
            
        } catch (error) {
            console.error("Error al reanudar el sistema:", error);
            this._showNotification("Error al reanudar el sistema", 'danger');
        } finally {
            this.state.is_loading = false;
        }
    }
}

// Registra el componente en el Systray de Odoo
console.log("SystrayButtons: Registrando componente en systray");
registry.category("systray").add("SystrayButtons", {
    Component: SystrayButtons,
}, { sequence: 120 });
console.log("SystrayButtons: Componente registrado");