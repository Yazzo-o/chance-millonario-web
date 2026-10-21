# Chance Millonario — acumulados y resultados

Página adaptable con acumulados grandes, tipografía gruesa, cápsulas moradas y bordes dorados. La web carga sus datos desde `data/resultados.json`.

## Activar GitHub Pages
1. Abre **Settings → Pages** de este repositorio.
2. En **Build and deployment**, elige **Deploy from a branch**.
3. Selecciona la rama `main` y la carpeta `/(root)`; guarda.
4. La URL esperada será https://yazzo-o.github.io/chance-millonario-web/

## Actualización diaria
El flujo `.github/workflows/actualizar.yml` está programado para ejecutarse cada día a las **06:15 a. m. de Colombia**. También se puede iniciar manualmente desde **Actions → Actualizar acumulados y resultados → Run workflow**.

El scraper valida los datos antes de escribirlos. Si una fuente cambia de estructura o no responde, conserva los últimos valores y registra el error en Actions en vez de inventar números.

## Fuentes oficiales
- https://supergirossucre.com.co/
- https://www.chancemillonario.com/index.php

## Primera prueba
Después de activar Pages, abre **Actions**, selecciona el flujo y pulsa **Run workflow**. Comprueba los logs y los valores extraídos antes de confiar en la actualización diaria; las fuentes pueden cambiar de HTML y requerir ajustes.
