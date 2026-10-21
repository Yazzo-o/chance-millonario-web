# SuperGIROS Alerta — MVP técnico

Este directorio contiene un punto de partida para una plataforma interna de simulacros sísmicos y evacuación para Android/iOS y panel web.

## Seguridad / estado
- Prototipo en desarrollo; no usar para emergencias reales.
- No envía notificaciones, mensajes de WhatsApp ni llamadas.
- No reemplaza alarmas físicas ni protocolos de SST.
- Recomendación: moverlo a un repositorio independiente privado antes de añadir código de producción.

## Arquitectura prevista
- App móvil: React Native
- Panel administrativo: React / Next.js
- Backend: Firebase Authentication, Cloud Functions, Firestore
- Push: Firebase Cloud Messaging + APNs
- Respaldo: proveedor de telefonía con llamadas automáticas, tras aprobación y pruebas
- Distribución privada: MDM corporativo, Apple Business Manager y Managed Google Play

## Siguiente etapa
1. Crear un repositorio privado independiente llamado `supergiros-alerta`.
2. Añadir backend y reglas de seguridad con acceso denegado por defecto.
3. Configurar autenticación y roles desde servidor.
4. Implementar alertas TEST solamente, sin envío a empleados.
5. Probar en emuladores y 20–30 dispositivos voluntarios.
6. Incorporar push y llamadas únicamente después de aprobación de SST y revisión de seguridad.

## Importante
No guardar credenciales, tokens push, teléfonos ni datos de empleados en Git. La entrega de notificaciones no es instantánea ni garantizada en todos los dispositivos.
