# Backend Firebase — SuperGIROS Alerta

## Alcance actual
La función `createTestAlert` solo guarda una alerta `TEST`. No envía notificaciones, WhatsApp ni llamadas.

## Requisitos
- Node.js 20+
- Firebase CLI
- Proyecto Firebase de desarrollo

## Comandos
```bash
npm install
npm run build
```

La función usa región `southamerica-east1`, requiere App Check y una sesión autenticada, y revisa el campo `role` en `users/{uid}`. Como las reglas de Firestore deniegan el acceso a clientes, el documento de rol debe crearse por un proceso administrativo seguro, nunca desde una app de empleado.

## Importante para pruebas
El archivo `src/index.test.ts` contiene pruebas unitarias de validación de tipo/texto. Para ejecutarlas tras compilar: `node --test lib/index.test.js`. Aún faltan pruebas de integración de Auth/Firestore Emulator y de autorización. No desplegar a producción ni activar llamadas externas hasta completar dichas pruebas y la revisión de SST/TI.