# Estado de implementación — 21 de octubre de 2026

## Publicado en GitHub
- Documentación de arquitectura.
- Reglas Firestore de denegación por defecto.
- Función callable `createTestAlert`, limitada a `TEST`.
- Panel web de demostración local.
- Plan de pruebas y guía de privacidad/operación.
- Pruebas unitarias iniciales de validación.

## No implementado todavía
- App móvil React Native compilable para Android/iOS.
- Firebase real configurado y desplegado.
- Autenticación corporativa/MDM.
- Envío push a dispositivos.
- Llamadas telefónicas y WhatsApp.
- Pruebas ejecutadas en CI y validación con móviles físicos.

## Decisión de repositorio
Los archivos se han añadido provisionalmente a `Yazzo-o/chance-millonario-web`, que es un repositorio público de Chance Millonario. Esto no es lo adecuado para una aplicación interna con datos operativos: crear un repositorio independiente **privado** `supergiros-alerta` y trasladar allí el código antes de introducir credenciales, identificadores de empleados o cualquier integración sensible.

El conector GitHub disponible permite escribir archivos en repositorios accesibles, pero no expone acción de crear un repositorio nuevo. No habilitar datos reales ni despliegue desde esta ubicación pública.