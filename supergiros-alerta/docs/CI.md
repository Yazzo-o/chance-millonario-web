# Validación local

## Panel web
Desde `supergiros-alerta/apps/admin-web`:

```bash
npm install
npm start
```

Abrir la URL local indicada por `serve` y verificar que el formulario crea un registro local marcado `LOCAL_DEMO_ONLY`; no se envía nada a empleados.

## Backend
Desde `supergiros-alerta/functions`:

```bash
npm install
npm run build
node --test lib/index.test.js
```

Las pruebas de autorización y Firestore requieren configurar Firebase Emulator e integración adicional. No declarar el backend listo para producción hasta que esas pruebas, el análisis de dependencias y una revisión de seguridad se completen.