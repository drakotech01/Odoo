# Módulo Systray Clock para Odoo 18

Este módulo añade un reloj en tiempo real a la barra de systray de Odoo.

## Características

- Muestra la hora actual del servidor en formato HH:MM:SS
- Actualización en tiempo real cada segundo
- Implementado con OWL (Odoo Web Library) para máximo rendimiento
- Diseño responsivo que se integra perfectamente con la interfaz de Odoo

## Instalación

1. Coloca la carpeta `systray_clock` en tu directorio de módulos de Odoo
2. Actualiza la lista de módulos desde la interfaz de administración
3. Instala el módulo "Systray Clock"

## Tecnologías utilizadas

- OWL (Odoo Web Library) para el componente frontend
- JavaScript ES6+ con sintaxis moderna
- XML para la definición de templates
- Bootstrap classes para el styling

## Estructura del código

El módulo sigue las mejores prácticas de desarrollo de Odoo:

1. **Separación de concerns**: Lógica JavaScript separada de la presentación XML
2. **Hooks de ciclo de vida**: Uso adecuado de onMounted y onWillUnmount
3. **Manejo de estado**: Utiliza el sistema de estado reactivo de OWL
4. **Manejo de recursos**: Limpieza adecuada de intervalos al desmontar el componente

## Personalización

Para modificar el formato de la hora, edita el método `getCurrentTime()` en `systray_clock.js`.