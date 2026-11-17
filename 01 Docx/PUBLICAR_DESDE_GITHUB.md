# Publicar la web desde este repositorio

Fecha de revisión: 17/11/2026.

Repositorio: https://github.com/adrianogstv/Resultados-MODFLOW

Web actual en Sites: https://wpc-kcb-evaluaciones-cifradas.saltymars15.chatgpt.site/

Hay dos rutas. **A** actualiza la dirección actual de Sites utilizando el contenido de GitHub. **B** permite crear otra publicación en GitHub Pages. El repositorio no tiene despliegue automático configurado: esta guía documenta los pasos, pero no los activa.

## 1. Obtener una versión concreta

Requiere Git y Python 3.9 o posterior. Para reconstruir no hacen falta paquetes Python adicionales, contraseña del visor ni modelos MODFLOW.

En una carpeta de trabajo nueva, ejecutar en PowerShell:

```powershell
git clone https://github.com/adrianogstv/Resultados-MODFLOW.git
Set-Location Resultados-MODFLOW
git switch main
git pull --ff-only
git rev-parse HEAD
```

Guardar el SHA que muestra el último comando: identifica la versión que se publicará. Si ya se dispone de un clon, entrar en él y actualizarlo con `git pull --ff-only` solo cuando sus cambios locales estén resueltos; no descartar trabajo para forzar la actualización.

## 2. Reconstruir y verificar

Desde la raíz del repositorio:

```powershell
python -B "00 Code/herramientas/preparar_publicacion.py" --salida "03 Output/PUBLICACION_MI_REVISION"
Get-Content "03 Output/PUBLICACION_MI_REVISION/VERIFICACION.json"
```

Elegir un nombre nuevo para cada revisión. El comando rechaza una carpeta existente para conservar las versiones anteriores. Si Windows usa el lanzador `py`, sustituir `python` por `py -3`.

La salida tiene esta estructura:

```text
03 Output/PUBLICACION_MI_REVISION/
  .openai/hosting.json
  dist/
    index.html
    app.js
    app.css
    crypto.json
    catalog.bin
    files/*.bin
  recursos_cifrados.zip
  VERIFICACION.json
```

Continuar únicamente si `VERIFICACION.json` muestra `status: PASS`. El proceso coteja los 840 archivos de la versión conservada y sus SHA-256. No descifra los recursos, no necesita la contraseña y no publica nada.

**La carpeta que sirve la web es `dist/`.** El ZIP ensamblado y la verificación son archivos de trabajo; no se sirven como parte de la web. La reconstrucción queda ignorada por Git mediante `03 Output/`.

## 3. Revisar en el navegador

```powershell
python -m http.server 8000 --directory "03 Output/PUBLICACION_MI_REVISION/dist"
```

Abrir http://localhost:8000. Introducir la contraseña únicamente en el visor. Comprobar apertura, selección de escenarios, cambio de figuras, descargas y botón de bloqueo. Detener ese servidor con Ctrl+C en su propia terminal.

Usar localhost o HTTPS: abrir `index.html` directamente con `file://` no reproduce el funcionamiento de las descargas y de Web Crypto.

## Ruta A. Actualizar la web actual en Sites

### Requisitos

La cuenta que publica debe tener acceso de propietario/editor al Site y disponer de la conexión Sites en Codex/ChatGPT. Tener acceso al repositorio público de GitHub no concede por sí solo acceso de publicación al Site.

La identidad conservada es:

```json
{
  "project_id": "appgprj_6adb901106488191aff5c0d1a12199f7",
  "static": {
    "directory": "dist"
  }
}
```

Está en [la configuración del repositorio](../.openai/hosting.json) y se copia a la carpeta generada. Conservar el `project_id` permite actualizar el mismo Site. No crear otro Site para reemplazar accidentalmente su dirección.

### Petición lista para usar en Codex

Pegar lo siguiente en un chat con acceso al repositorio y a Sites. Sustituir `SHA_A_PUBLICAR` por el SHA registrado en el paso 1:

> Publica la versión SHA_A_PUBLICAR de https://github.com/adrianogstv/Resultados-MODFLOW en el Site existente appgprj_6adb901106488191aff5c0d1a12199f7. Sigue 01 Docx/PUBLICAR_DESDE_GITHUB.md y la skill Sites disponible. Clona o abre esa versión y reconstruye la web con 00 Code/herramientas/preparar_publicacion.py en una salida nueva. Exige VERIFICACION.json con PASS. Abre el proyecto administrado del mismo Site y prepara su versión estática con el contenido de dist, conservando la identidad y los demás campos de configuración. Usa el flujo autorizado de sincronización, empaquetado, guardado y despliegue de Sites. Conserva la audiencia actual, el cifrado y la dirección publicada. No publiques modelos, archivos descifrados ni contraseñas. Al terminar informa URL, SHA de GitHub, versión guardada y estado del despliegue. No crees automatizaciones.

### Qué debe realizar quien publica

1. Consultar el Site existente y confirmar identidad, permisos y audiencia.
2. Reconstruir el SHA elegido y revisar el resultado.
3. Abrir el repositorio administrado de Sites mediante su herramienta/skill. GitHub y ese repositorio administrado son distintos; un `git push` a este GitHub no actualiza el segundo.
4. Incorporar el contenido generado de `dist/` y mantener `static.directory` apuntando a ese directorio. Conservar otros campos necesarios de la configuración del Site.
5. Usar el flujo de Sites para sincronizar su fuente, crear el paquete, guardar una versión y desplegarla con la audiencia vigente. Las credenciales de Sites se obtienen mediante la conexión; no se guardan aquí.
6. Esperar el resultado terminal de la publicación y registrar URL, SHA de GitHub, versión de Sites y estado.

Para entregar a otra persona el paquete reconstruido, incluir `dist/` y `.openai/hosting.json` juntos como proyecto. No basta con enviar únicamente `index.html`. La persona que publique debe tener los permisos del Site correspondiente.

## Ruta B. Publicar otra dirección con GitHub Pages

Esta alternativa es opcional. Crea una dirección distinta y no actualiza ni sustituye el enlace de Sites. **No se ha activado al añadir esta guía.**

1. En GitHub, abrir este repositorio y entrar en **Settings → Pages**.
2. En **Build and deployment → Source**, seleccionar **GitHub Actions**.
3. Crear `.github/workflows/publicar-pages.yml` con el ejemplo siguiente. Se ejecuta manualmente; no publica por cada push.

```yaml
name: Publicar visor en GitHub Pages

on:
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: github-pages
  cancel-in-progress: false

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Obtener el repositorio
        uses: actions/checkout@v6
      - name: Preparar Pages
        uses: actions/configure-pages@v5
      - name: Reconstruir y comprobar recursos cifrados
        run: python3 -B "00 Code/herramientas/preparar_publicacion.py" --salida "03 Output/PAGES"
      - name: Subir solo la carpeta web
        uses: actions/upload-pages-artifact@v4
        with:
          path: "03 Output/PAGES/dist"
      - name: Publicar
        id: deployment
        uses: actions/deploy-pages@v4
```

4. Confirmar ese archivo en GitHub. En **Actions**, abrir el workflow, seleccionar la rama y pulsar **Run workflow**.
5. Esperar a que termine correctamente y abrir la URL que devuelva el despliegue. Para el nombre actual, la dirección esperada es `https://adrianogstv.github.io/Resultados-MODFLOW/`; no se afirma que esté activa hasta completar esa publicación.

No publicar la raíz del repositorio como artefacto: allí no está la web reconstruida. El workflow sirve exclusivamente `03 Output/PAGES/dist`. GitHub Pages no necesita el `project_id` de Sites ni la contraseña del visor como secreto de Actions. El visitante introduce su contraseña en la interfaz; los recursos siguen cifrados.

El YAML es una receta documentada, no un workflow instalado ni un despliegue verificado en esta revisión. Los componentes de Actions siguen el ejemplo oficial vigente consultado en la fecha de esta guía.

## Actualizaciones y problemas habituales

| Situación | Qué hacer |
|---|---|
| Solo se ha hecho `git push` | El código está versionado. Actualizar Sites por la ruta A o ejecutar Pages si se configuró la ruta B. |
| La salida ya existe | Usar otra carpeta de `03 Output`; conservar la anterior. |
| Falta una parte o no coincide un hash | Confirmar que el clon tiene todos los archivos de la misma versión. No desactivar el control ni corregir hashes sin revisar el origen. |
| Se ha editado HTML, JS, CSS o un recurso | El manifiesto describe bytes concretos. Preparar y revisar una versión coherente del manifiesto y, si corresponde, del paquete cifrado antes de reconstruir. Esta guía no incluye un generador de resultados científicos ni de nuevos paquetes cifrados. |
| Sites indica falta de acceso | Revisar la cuenta y permisos de Sites. La sesión de GitHub no sustituye esa autorización. |
| GitHub devuelve 403 al subir código | Revisar el acceso de escritura de la integración o la autenticación Git local. No pegar tokens en issues, README o chats. |
| El visor no abre con doble clic | Servir `dist/` por localhost o HTTPS. |
| Se quiere volver a una versión anterior | Reconstruir su SHA en una copia de trabajo nueva y publicar esa versión con la misma identidad. Conservar las versiones actuales y los archivos previos. |

La copia del repositorio preserva la publicación respaldada el 17/11/2026. Reconstruirla no incorpora automáticamente la última entrega local de modelos ni los objetivos de calibración.

## Referencias oficiales

- [Crear y utilizar ChatGPT Sites](https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites).
- [Configurar la fuente de publicación de GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
- [Ejemplo oficial de despliegue con GitHub Actions](https://docs.github.com/en/get-started/start-your-journey/deploying-your-website-automatically).
