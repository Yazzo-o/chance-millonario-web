# Seguridad y salida a producción

## Estado del MVP
El panel web actual es una demostración local, no una herramienta de emergencia. La función callable solo registra eventos `TEST` y no envía mensajes por canales externos.

## Antes de conectar dispositivos
- Configurar Firebase App Check para las plataformas reales.
- Configurar autenticación corporativa y MFA para administradores.
- Definir un procedimiento supervisado para conceder y revocar los roles.
- Revisar datos personales, base legal, retención y acceso con TI/Jurídica.
- Proteger tokens push y teléfonos; nunca ponerlos en registros públicos.
- Añadir auditoría y alertas de fallo de los propios servicios.

## Antes de activar un simulacro real
- Aprobación formal de SST y responsables de la sede.
- Comprobación independiente del contenido, destinatarios y hora.
- Procedimiento de cancelación y comunicación de cierre.
- Pruebas de extremo a extremo en dispositivos de control.
- Canales alternativos si la red, los teléfonos o los servicios cloud fallan.

## Advertencias de plataforma
Las notificaciones push no garantizan entrega inmediata. El sonido depende de permisos, configuración, conexión y sistema operativo. iOS Critical Alerts requiere entitlement aprobado por Apple. La distribución privada se configura por separado con el MDM corporativo.

No habilitar llamadas masivas ni usar el MVP como sistema único de seguridad humana.
