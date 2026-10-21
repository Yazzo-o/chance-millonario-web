# SuperGIROS Alerta — MVP técnico

Punto de partida para una plataforma interna de simulacros sísmicos y evacuación para Android/iOS y panel web.

## Importante
- Esta versión es un **MVP de desarrollo**.
- La interfaz web registra demostraciones locales únicamente.
- La función de backend solo registra alertas de tipo `TEST` y **no envía push, WhatsApp ni llamadas**.
- No usar para emergencias reales ni reemplazar alarmas físicas o protocolos de SST.

## Arquitectura prevista
- App móvil: React Native
- Panel: web
- Backend: Firebase Authentication, Cloud Functions v2 y Firestore
- Push: Firebase Cloud Messaging + APNs
- Llamadas: proveedor de telefonía con sandbox primero
- Distribución privada: MDM corporativo, Apple Business Manager y Managed Google Play

## Estructura
- `apps/admin-web/`: panel demostrativo local.
- `functions/`: función callable de prueba, protegida por autenticación, rol y App Check.
- `firebase/firestore.rules`: denegación de acceso cliente por defecto.
- `docs/`: arquitectura y plan de pruebas.

## Preparación local
1. Instala Node.js 20+ y Firebase CLI.
2. Instala dependencias: `cd supergiros-alerta/functions && npm install`.
3. Configura un proyecto de Firebase de desarrollo y revisa la configuración de emuladores.
4. Antes de desplegar, añade aprovisionamiento seguro de roles en `users/{uid}`; nunca habilites que el cliente escriba su propio rol.
5. Ejecuta `npm run build` dentro de `functions`.
6. Despliega únicamente a un proyecto de desarrollo tras revisar permisos, reglas y costes.

## Función backend
`createTestAlert`:
- requiere autenticación;
- exige rol `sst_admin` o `system_admin` en el documento `users/{uid}`;
- exige App Check;
- acepta exclusivamente `type: "TEST"`;
- registra hora del servidor;
- no genera mensajes externos.

Las reglas de Firestore deniegan el acceso desde clientes por defecto. Cloud Functions usa Admin SDK y debe validar roles explícitamente.

## Siguientes pasos
1. Configurar Firebase Authentication y el flujo administrado de asignación de roles.
2. Añadir pruebas automatizadas de autorización y validación.
3. Conectar la aplicación móvil y registro seguro de tokens push.
4. Implementar una cola con idempotencia, reintentos limitados y estados reales de entrega.
5. Probar con 20–30 dispositivos antes de ampliar.
6. Añadir llamadas solo después de validar el flujo con un proveedor en sandbox y aprobación de SST.
7. Configurar distribución privada mediante MDM.

## Límites
La recepción depende de conectividad, permisos, batería, sistema operativo y servicios push. No se puede garantizar un sonido audible en todos los dispositivos. Mantén canales físicos y procedimientos alternativos.
