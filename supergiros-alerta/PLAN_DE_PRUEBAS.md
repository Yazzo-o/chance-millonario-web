# Plan de pruebas — SuperGIROS Alerta

## Seguridad
- [ ] Sin sesión no se puede crear una alerta.
- [ ] Rol empleado no puede activar alertas.
- [ ] Cliente no puede leer/escribir directamente colecciones protegidas.
- [ ] En MVP, solo se admite `TEST`.
- [ ] Texto, tamaños y sede se validan en servidor.
- [ ] App Check/MFA y auditoría configurados antes del entorno de empresa.

## Funcionalidad
- [ ] La alerta queda registrada con hora del servidor y autor.
- [ ] Estados separados: creada, enviada, entrega informada, recepción confirmada, llegada confirmada.
- [ ] Reintentos idempotentes y sin duplicar confirmaciones.
- [ ] Fallos de push aparecen como pendientes, no como recibidos.

## Móviles
- [ ] Android: primer plano, segundo plano, app cerrada, ahorro de batería y permisos denegados.
- [ ] iOS: primer plano, segundo plano, app cerrada, modos de concentración y permisos.
- [ ] Wi-Fi/datos, conectividad intermitente y token inválido.
- [ ] Probar vibración/sonido por dispositivo; nunca asumir sonido garantizado.

## Carga y operación
- [ ] Simular 500 destinatarios sin enviar mensajes externos.
- [ ] Medir latencia, errores, reintentos, duplicados y confirmaciones.
- [ ] Piloto anunciado con 20–30 personas voluntarias y autorización de SST.
- [ ] Probar llamadas solo con sandbox y teléfonos de prueba autorizados.
- [ ] Ensayar procedimiento alternativo si internet o servicios push fallan.

## Gate de producción
No habilitar SIMULACRO/EMERGENCIA ni llamadas masivas hasta tener revisión técnica, aprobación formal de SST, procedimiento operativo y distribución MDM validada.
