/** @odoo-module **/
import { rpc } from "@web/core/network/rpc";

console.log("✅ Geo Button cargado correctamente");

// Variables globales pero vacías
let lat = null;
let lng = null;

async function getLocationAndSave() {
  if (!navigator.geolocation) {
    alert("Geolocalización no soportada por este navegador.");
    return;
  }

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      // Asignamos valores en el momento de la acción
      lat = position.coords.latitude;
      lng = position.coords.longitude;

      console.log("📍 Coordenadas capturadas:", lat, lng);

      try {
        const result = await rpc(
          "/web/dataset/call_kw/geo.location/guardar_coordenadas",
          {
            model: "geo.location",
            method: "guardar_coordenadas",
            args: [lat, lng],
            kwargs: {},
          }
        );
        
        console.log("✅ Guardado en servidor:", result);
        alert(`Guardado en Odoo: ${lat}, ${lng}`);
        window.location.reload(); // Recargar la página
      } catch (error) {
        console.error("❌ Error al guardar coordenadas:", error);
        alert("Error al guardar en Odoo");
      }
    },
    (error) => {
      console.error("❌ Error al obtener ubicación:", error);
      alert("No se pudo obtener la ubicación.");
    }
  );
}

// Asignar función al botón
window.obtenerUbicacionOriginal = getLocationAndSave;
