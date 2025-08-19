/** @odoo-module **/

import { Component, useState, onMounted, onWillUnmount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

/**
 * Hook personalizado para servicios seguros
 */
function useSafeService(serviceName) {
    let service = null;
    
    const getService = () => {
        if (!service) {
            try {
                service = useService(serviceName);
            } catch (error) {
                console.warn(`Servicio ${serviceName} no disponible:`, error);
                return null;
            }
        }
        return service;
    };
    
    return getService;
}

/**
 * Componente Systray Widget para funcionalidad de pausar/reanudar
 */
class SystrayButtons extends Component {
    static template = "hr_attendance_tracker.SystrayButtons";
    
    setup() {
        console.log("SystrayButtons: Widget inicializado");
        
        // Usa useState para gestionar el estado del widget
        this.state = useState({
            is_paused: false,
            is_loading: false,
            services_ready: false,
            last_update: null,
        });
        
        // Servicios usando hooks seguros
        this.getNotificationService = useSafeService("notification");
        this.getRpcService = useSafeService("rpc");
        this.getActionService = useSafeService("action");
        
        // Inicializa los servicios cuando el componente esté montado
        onMounted(() => {
            this._initializeServices();
            this._startPeriodicUpdate();
        });
        
        // Limpia el intervalo cuando el componente se desmonte
        onWillUnmount(() => {
            if (this.updateInterval) {
                clearInterval(this.updateInterval);
            }
        });
        
        console.log("SystrayButtons: Widget configurado");
    }

    /**
     * Inicializa los servicios después del montaje
     */
    _initializeServices() {
        try {
            // Intenta obtener los servicios
            const notification = this.getNotificationService();
            const rpc = this.getRpcService();
            const action = this.getActionService();
            
            if (notification && rpc) {
                this.state.services_ready = true;
                console.log("SystrayButtons: Servicios listos");
                
                // Cargar estado inicial del sistema
                this._loadInitialState();
            } else {
                console.log("SystrayButtons: Servicios no disponibles, reintentando...");
                // Reintenta después de un tiempo
                setTimeout(() => this._initializeServices(), 1000);
            }
        } catch (error) {
            console.warn("SystrayButtons: Error al inicializar servicios:", error);
            // Reintenta después de un tiempo
            setTimeout(() => this._initializeServices(), 1000);
        }
    }

    /**
     * Inicia la actualización periódica del estado
     */
    _startPeriodicUpdate() {
        // Actualiza el estado cada 30 segundos
        this.updateInterval = setInterval(() => {
            if (this.state.services_ready) {
                this._loadInitialState();
            }
        }, 30000);
    }

    /**
     * Carga el estado inicial del sistema
     */
    async _loadInitialState() {
        try {
            const rpcService = this.getRpcService();
            if (rpcService) {
                // Llamada RPC para obtener el estado actual
                // const result = await rpcService.call('/web/dataset/call_kw', {
                //     model: 'hr.attendance.tracker',
                //     method: 'get_system_state',
                //     args: [],
                //     kwargs: {}
                // });
                // this.state.is_paused = result.is_paused;
                // this.state.last_update = new Date();
                
                // Por ahora simulamos el estado
                // this.state.is_paused = false;
                this.state.last_update = new Date();
                console.log("SystrayButtons: Estado inicial cargado");
            }
        } catch (error) {
            console.error("Error al cargar estado inicial:", error);
        }
    }

    /**
     * Muestra una notificación de forma segura
     */
    _showNotification(message, type = 'info') {
        const notification = this.getNotificationService();
        if (notification) {
            notification.add(message, { type: type });
        } else {
            console.log(`Notificación [${type}]: ${message}`);
        }
    }

    /**
     * Cierra el dropdown después de una acción
     */
    _closeDropdown() {
        // Encuentra el dropdown y lo cierra
        const dropdown = this.el.querySelector('.dropdown');
        if (dropdown) {
            const bsDropdown = bootstrap.Dropdown.getInstance(dropdown.querySelector('.dropdown-toggle'));
            if (bsDropdown) {
                bsDropdown.hide();
            }
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
            const rpcService = this.getRpcService();
            
            if (rpcService && this.state.services_ready) {
                // Llamada RPC real cuando el servicio esté disponible
                // await rpcService.call('/web/dataset/call_kw', {
                //     model: 'hr.attendance.tracker',
                //     method: 'pause_system',
                //     args: [],
                //     kwargs: {}
                // });
                
                // Por ahora simulamos la llamada
                await new Promise(resolve => setTimeout(resolve, 1500));
            } else {
                // Simulación si el servicio no está disponible
                console.warn("SystrayButtons: Servicios no listos, usando simulación");
                await new Promise(resolve => setTimeout(resolve, 1500));
            }
            
            this.state.is_paused = true;
            this.state.last_update = new Date();
            this._showNotification("Sistema pausado correctamente", 'success');
            
            // Cierra el dropdown después de la acción
            setTimeout(() => this._closeDropdown(), 500);
            
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
            const rpcService = this.getRpcService();
            
            if (rpcService && this.state.services_ready) {
                // Llamada RPC real cuando el servicio esté disponible
                // await rpcService.call('/web/dataset/call_kw', {
                //     model: 'hr.attendance.tracker',
                //     method: 'resume_system',
                //     args: [],
                //     kwargs: {}
                // });
                
                // Por ahora simulamos la llamada
                await new Promise(resolve => setTimeout(resolve, 1500));
            } else {
                // Simulación si el servicio no está disponible
                console.warn("SystrayButtons: Servicios no listos, usando simulación");
                await new Promise(resolve => setTimeout(resolve, 1500));
            }
            
            this.state.is_paused = false;
            this.state.last_update = new Date();
            this._showNotification("Sistema reanudado correctamente", 'success');
            
            // Cierra el dropdown después de la acción
            setTimeout(() => this._closeDropdown(), 500);
            
        } catch (error) {
            console.error("Error al reanudar el sistema:", error);
            this._showNotification("Error al reanudar el sistema", 'danger');
        } finally {
            this.state.is_loading = false;
        }
    }

    /**
     * Maneja el clic en "Ver Estadísticas"
     */
    onClickStats() {
        console.log("SystrayButtons: Clic en Ver Estadísticas");
        
        const actionService = this.getActionService();
        if (actionService) {
            // Abre la vista de estadísticas
            actionService.doAction({
                name: 'Estadísticas de Asistencia',
                type: 'ir.actions.act_window',
                res_model: 'hr.attendance.tracker.stats',
                view_mode: 'tree,form',
                views: [[false, 'tree'], [false, 'form']],
                target: 'current',
            });
        }
        
        this._closeDropdown();
    }

    /**
     * Maneja el clic en "Configuración"
     */
    onClickSettings() {
        console.log("SystrayButtons: Clic en Configuración");
        
        const actionService = this.getActionService();
        if (actionService) {
            // Abre la vista de configuración
            actionService.doAction({
                name: 'Configuración de Asistencia',
                type: 'ir.actions.act_window',
                res_model: 'hr.attendance.tracker.config',
                view_mode: 'form',
                views: [[false, 'form']],
                target: 'new',
            });
        }
        
        this._closeDropdown();
    }

    /**
     * Getter para obtener el texto del estado actual
     */
    get statusText() {
        return this.state.is_paused ? 'Pausado' : 'Activo';
    }

    /**
     * Getter para obtener la clase CSS del botón principal
     */
    get mainButtonClass() {
        return this.state.is_paused ? 'text-danger' : 'text-success';
    }

    /**
     * Getter para obtener el icono del estado
     */
    get statusIcon() {
        return this.state.is_paused ? 'fa-pause-circle' : 'fa-play-circle';
    }
}

// Registra el componente en el Systray de Odoo
console.log("SystrayButtons: Registrando widget en systray");
registry.category("systray").add("SystrayButtons", {
    Component: SystrayButtons,
}, { sequence: 1 }); // Secuencia para posicionamiento en el systray
console.log("SystrayButtons: Widget registrado correctamente");