/** @odoo-module **/
console.log("✅ Geo Capture cargado correctamente");

import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { rpc } from "@web/core/network/rpc";
import { _t } from "@web/core/l10n/translation";
import { Dialog } from "@web/core/dialog/dialog";

// Patch al controlador del formulario
patch(FormController.prototype, {
    async onClickButton(params) {
        if (params?.attrs?.name === 'action_get_browser_location') {
            if (!navigator.geolocation) {
                Dialog.alert(this, _t("Este navegador no soporta geolocalización."));
                return;
            }

            navigator.geolocation.getCurrentPosition(
                async (position) => {
                    const lat = position.coords.latitude;
                    const lng = position.coords.longitude;

                    // Actualiza el modelo con las coordenadas
                    await this.model.root.update({
                        latitude: lat,
                        longitude: lng,
                    });

                    // Guarda el registro automáticamente
                    await this.model.save();
                },
                (error) => {
                    Dialog.alert(this, _t("No se pudo obtener la ubicación: ") + error.message);
                }
            );
        } else {
            // Para otros botones, comportamiento normal
            await super.onClickButton(params);
        }
    },
});