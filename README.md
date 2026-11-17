# Resultados-MODFLOW

Código y recursos cifrados del visor de resultados **WPC KCB**.

También sirve como guía para que compañeros publiquen sus propios dashboards en cuentas bajo su control.

**Empieza aquí: [paso a paso para compañeros, actualizaciones y límites de GitHub](01%20Docx/PASO_A_PASO_PARA_COMPANEROS.md).**

Cada dashboard nuevo debe tener su propio repositorio y datos: esta guía no requiere copiar los resultados WPC. La web de este repositorio conserva su configuración actual.

**Retiro de OpenAI Sites:** [estado pendiente y pasos para eliminar solo el sitio antiguo](01%20Docx/RETIRAR_SITIO_ANTIGUO_OPENAI.md).

**Web en GitHub Pages:** https://adrianogstv.github.io/Resultados-MODFLOW/

**[Guía de la web y reconstrucción](01%20Docx/GUIA_WEB.md)**

**[Cómo publicar y actualizar en GitHub Pages](01%20Docx/PUBLICAR_DESDE_GITHUB.md)**

El frontend está en `00 Code/visor`; las instrucciones en `01 Docx`; los parámetros públicos y recursos cifrados en `02 Input`. Las reconstrucciones locales se guardan en `03 Output`.

```powershell
python -B "00 Code/herramientas/preparar_publicacion.py"
```

La reconstrucción verifica los840 archivos de la publicación conservada y no requiere la contraseña. La contraseña se introduce únicamente al abrir el visor; no está guardada aquí.

GitHub conserva el código, los recursos cifrados y el alojamiento mediante GitHub Pages. Los cambios en código/recursos de `main` ejecutan `.github/workflows/publicar-pages.yml`. También se puede publicar manualmente desde Actions. Las modificaciones documentales no vuelven a desplegar la web.

Esta migración conserva los resultados de la publicación respaldada; no incorpora entregas científicas locales posteriores. La antigua configuración de Sites queda archivada y ya no se usa para reconstruir ni desplegar.

No incluye archivos nativos MODFLOW ni figuras/tablas descifradas. Los datos cifrados se conservan en34 partes pequeñas con un manifiesto SHA-256 para reconstruirlos sin descargar recursos externos.

## Publicar otros dashboards

[Guía reutilizable para Claude, Codex y usuarios: GitHub Pages, Cloudflare Pages, Netlify, Vercel y servidor propio](01%20Docx/PUBLICAR_DASHBOARDS_MULTIPLATAFORMA.md). Incluye elección del destino, preparación, publicación, verificación y un prompt para reutilizar. Los agentes encuentran la entrada en AGENTS.md y CLAUDE.md.
