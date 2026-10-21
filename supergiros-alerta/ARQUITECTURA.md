# Arquitectura inicial — SuperGIROS Alerta

## Flujo
1. Usuario corporativo autenticado entra al panel.
2. El servidor comprueba el rol y registra el evento con hora del servidor.
3. En MVP, solo se permite `TEST`; no hay difusión externa.
4. En fase siguiente, una cola con idempotencia distribuirá push a dispositivos activos.
5. La app registrará `receivedAt` tras acción del usuario y `assemblyPointAt` al confirmar llegada.
6. El panel SST mostrará pendientes; llamadas de voz se usarán solo tras el umbral aprobado y con sandbox probado.

## Componentes
- Mobile: React Native y módulos nativos para APNs/FCM.
- Admin: panel web con roles.
- Backend: Firebase Authentication, Cloud Functions v2, Firestore.
- Push: FCM en Android y APNs en iOS a través de FCM.
- Voz: proveedor SIP/CPaaS con lista autorizada, límites de frecuencia y entorno de pruebas.
- Gestión: MDM corporativo; aplicación privada en Apple Business Manager y Managed Google Play.

## Esquema sugerido
- `users/{uid}`: `role`, `active`, `siteId`, `employeeId` mínimo necesario.
- `devices/{deviceId}`: `uid`, `platform`, `token`, `appVersion`, `lastSeenAt`, `active`.
- `alerts/{alertId}`: `type`, `status`, `title`, `message`, `createdBy`, `createdAt`, `siteId`.
- `acknowledgments/{alertId_uid}`: `alertId`, `uid`, `receivedAt`, `assemblyPointAt`, `clientEventId`.

## Seguridad
- Firestore deniega lecturas/escrituras cliente por defecto.
- Roles comprobados en servidor; nunca aceptar autoasignación de rol del cliente.
- App Check, MFA para administradores, registro de auditoría y secretos fuera del repositorio.
- Idempotencia por evento y destinatario para reducir duplicados.
- No recopilar GPS continuo por defecto.
- Separar visualmente y en permisos `TEST`, `SIMULACRO` y `EMERGENCIA`.

## Condiciones antes de producción
- Visto bueno de SST, TI, Jurídica/Privacidad y responsables de continuidad.
- Probar con teléfonos de control; no realizar llamadas masivas durante el desarrollo.
- Medir latencias y confirmaciones; no presentar el envío como prueba de recepción.
- No depender solo de móviles: mantener alarma física y procedimiento alterno.
- Solicitar a Apple entitlement Critical Alerts por la vía oficial; no asumir que será concedido.
