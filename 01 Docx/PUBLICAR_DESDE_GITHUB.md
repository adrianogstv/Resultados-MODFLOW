# Publicar y actualizar en GitHub Pages

Fecha: 17/11/2026.

Web principal: https://adrianogstv.github.io/Resultados-MODFLOW/

Repositorio: https://github.com/adrianogstv/Resultados-MODFLOW

El alojamiento y el despliegue se realizan en GitHub Pages y GitHub Actions. No se necesita Sites para reconstruir o publicar esta versión. El archivo .openai/hosting.json se conserva únicamente como registro histórico archivado y el constructor no lo utiliza.

## Publicación automática

1. Modificar y revisar el código o los recursos cifrados en una copia de trabajo del repositorio.
2. Mantener la coherencia con el manifiesto SHA-256 de02 Input/publicacion/MANIFIESTO.json. Una modificación de archivos protegidos por el manifiesto requiere una nueva preparación revisada; no desactivar verificaciones.
3. Confirmar los cambios y subirlos a main.
4. Abrir Actions y seguir el workflow «Publicar visor en GitHub Pages».
5. Esperar que todas las etapas terminen correctamente. El workflow obtiene el código, verifica y reconstruye los840 archivos, sube únicamente dist y publica.
6. Abrir la web y revisar selección de escenarios, figuras, descargas y bloqueo.

El workflow activo está en [.github/workflows/publicar-pages.yml](../.github/workflows/publicar-pages.yml). Se ejecuta por cambios en00 Code,02 Input o en el propio workflow. Los cambios de documentación no despliegan por sí solos.

## Publicación manual de una rama

En GitHub: **Actions → Publicar visor en GitHub Pages → Run workflow**. Seleccionar la rama y ejecutar. La configuración del repositorio usa **Settings → Pages → Source: GitHub Actions**.

No se necesitan credenciales de Sites ni la contraseña del visor como secreto de Actions. GitHub gestiona la autorización del despliegue mediante su token y entorno github-pages.

## Revisar localmente antes de publicar

Con Git y Python3.9 o posterior, en una carpeta nueva:

```powershell
git clone https://github.com/adrianogstv/Resultados-MODFLOW.git
Set-Location Resultados-MODFLOW
git rev-parse HEAD
python -B "00 Code/herramientas/preparar_publicacion.py" --salida "03 Output/REVISION_NUEVA"
Get-Content "03 Output/REVISION_NUEVA/VERIFICACION.json"
python -m http.server 8000 --directory "03 Output/REVISION_NUEVA/dist"
```

Abrir http://localhost:8000. Usar una salida nueva en cada ejecución. El proceso conserva resultados anteriores y exige PASS. La salida contiene dist, un ZIP cifrado de trabajo y la verificación; solo dist se publica. Si se usa el lanzador de Windows, sustituir python por py -3.

Para actualizar un clon existente con trabajo local resuelto, usar git pull --ff-only. No descartar archivos para forzar una actualización. Conservar el SHA asociado a cada publicación; el workflow y su artefacto permiten identificar la versión exacta desplegada.

## Alcance y protección

El repositorio mantiene el frontend y los recursos cifrados de la publicación respaldada. No contiene modelos MODFLOW ni originales descifrados. La contraseña se introduce únicamente en el visor; nunca en commits, instrucciones, issues o workflows.

Los enlaces a recursos son relativos y funcionan bajo /Resultados-MODFLOW/. No usar la raíz del repositorio como artefacto de Pages: allí están el código y las partes cifradas, no la web ensamblada. Abrir index.html con file:// tampoco equivale a servirla por HTTPS o localhost.

La migración de alojamiento no incorpora automáticamente los resultados de entregas locales posteriores ni los objetivos de calibración. Generar una nueva entrega científica es una tarea distinta.

## Errores habituales y recuperación

- Hash o parte incorrecta: revisar que todos los archivos sean de la misma versión; no omitir controles.
- Carpeta existente: escoger otra salida, sin borrar la anterior.
- Error de despliegue: revisar el job y los pasos de Actions antes de reintentar.
- Acceso a Pages: confirmar que Source es GitHub Actions y que el workflow tiene contents:read, pages:write e id-token:write.
- Volver a una versión anterior: recuperar y revisar su contenido en una copia nueva y generar un commit de recuperación. Conservar el historial y las salidas anteriores; no forzar la rama ni borrar versiones para retroceder.

## Referencias

- [Configurar la fuente de GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
- [Desplegar con GitHub Actions](https://docs.github.com/en/get-started/start-your-journey/deploying-your-website-automatically).
