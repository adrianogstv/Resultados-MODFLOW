# Publicar dashboards en una cuenta propia

Guía para personas, Claude y Codex. Revisada el 17/11/2026. Este documento no cambia el alojamiento por sí solo.

## Empezar aquí

Leer primero AGENTS.md y README.md del proyecto. Identificar si el dashboard es estático (HTML, CSS, JavaScript y archivos) o necesita un servidor (Python, base de datos, API, autenticación). Los cuatro proveedores siguientes sirven para contenido estático; una aplicación con servidor requiere evaluar su runtime y servicios por separado.

GitHub guarda y versiona el código; el proveedor sirve la web. Pueden ser empresas distintas. Usar siempre cuentas, repositorios y dominios del usuario, para que conserve el control. No publicar en OpenAI Sites salvo petición explícita.

Si no existe una elección previa, preguntar una sola vez: «¿Dónde quieres alojarlo: GitHub Pages, Cloudflare Pages, Netlify, Vercel o tu propio servidor? ¿En qué cuenta/proyecto y con qué acceso?». No crear varios sitios para probar ni cambiar el proveedor de una web existente sin indicación. Si el destino ya fue elegido, continuar sin volver a preguntarlo.

## Elegir el destino

| Destino | Cuándo considerarlo | Forma de entrega |
|---|---|---|
| GitHub Pages | Dashboard estático vinculado al repositorio | GitHub Actions publica un artefacto estático |
| Cloudflare Pages | Web estática con cuenta y dominio del usuario en Cloudflare | Integración Git o carga directa de archivos construidos |
| Netlify | Web estática con despliegues previos de revisión | Integración Git o carga manual de la carpeta final |
| Vercel | Web estática o frontend con framework | Importación Git o despliegue por CLI desde la cuenta del usuario |
| Servidor propio | Se requiere control de infraestructura o un backend específico | Configurar HTTPS, servidor web, acceso y actualizaciones |

Comprobar los términos, límites de archivos, tráfico, compilación, acceso y uso comercial vigentes antes de elegir. No prometer gratuidad ilimitada ni activar cobros sin autorización. Un dominio propio se configura después de verificar el sitio y requiere control del DNS; no es obligatorio para publicar.

## Preparar una entrega portable

1. Separar código, documentación, entradas y resultados según la estructura del proyecto. En este repositorio: 00 Code, 01 Docx, 02 Input y 03 Output.
2. Construir una carpeta publicable con index.html en su raíz y todos los recursos necesarios. Publicar exclusivamente esa carpeta, nunca el repositorio completo.
3. Usar rutas web relativas, no rutas de discos locales. Comprobar mayúsculas/minúsculas, espacios y funcionamiento bajo una subruta, especialmente en GitHub Pages.
4. Identificar dependencias externas, claves y datos sensibles. Un archivo servido por una web estática puede descargarse: ocultar un enlace o poner un formulario de contraseña no protege datos en claro. Conservar cifrado real o elegir control de acceso del proveedor según la necesidad.
5. No guardar contraseñas, tokens ni claves en Git, JavaScript público, argumentos o logs. Autenticarse con las herramientas oficiales en la cuenta del usuario; para CI utilizar el almacén de secretos del proveedor cuando haga falta.
6. No borrar ni mover archivos anteriores. Crear salidas nuevas y preservar versiones de recuperación.

### Constructor de este visor WPC

Desde la raíz del repositorio, con Python 3.9 o posterior:

```powershell
python -B "00 Code/herramientas/preparar_publicacion.py" --salida "03 Output/ENTREGA_NUEVA"
```

Elegir un nombre de salida que todavía no exista. La carpeta publicable será `03 Output/ENTREGA_NUEVA/dist`. El constructor verifica 840 archivos y sus hashes; no descifra los resultados ni requiere contraseña. Estas cifras y este comando pertenecen a este visor: para otro dashboard se debe identificar su constructor, no copiar sus recursos o manifiesto.

## GitHub Pages

Para esta web ya está elegido y configurado: https://adrianogstv.github.io/Resultados-MODFLOW/ . Seguir [PUBLICAR_DESDE_GITHUB.md](PUBLICAR_DESDE_GITHUB.md) y el workflow existente; no crear otro proyecto.

Para un nuevo dashboard: crear o seleccionar el repositorio del usuario, configurar Pages para desplegar mediante GitHub Actions, construir el dashboard en el workflow y subir solo la carpeta final con upload-pages-artifact; publicar con deploy-pages. Otorgar únicamente los permisos necesarios, incluidos pages: write e id-token: write para ese flujo. Verificar la URL real entregada por el despliegue y el funcionamiento en la subruta del repositorio. No asumir que la privacidad del repositorio hace privada la web.

## Cloudflare Pages

En Workers & Pages de la cuenta del usuario, crear o seleccionar un proyecto Pages. Elegir integración con el repositorio Git o carga directa. Para una carpeta estática ya construida, cargar solo su contenido final; no indicar un constructor que no existe. Para integración Git, definir rama de producción, comando real de construcción y directorio de salida relativo a la raíz configurada. Confirmar que el entorno dispone del runtime necesario. La elección entre carga directa e integración Git tiene restricciones de cambio: revisarlas antes de crear el proyecto.

En este visor es posible construir localmente con el comando anterior y cargar dist; para automatizar la reconstrucción remota, adaptar el nombre de salida a un entorno nuevo y comprobar Python y hashes. No introducir credenciales de Cloudflare en el repositorio.

## Netlify

Para publicación manual, construir primero en local y cargar la carpeta final que contiene index.html, desde la cuenta del usuario. La carga manual no ejecuta el constructor. Para actualizaciones continuas, importar el repositorio, seleccionar la rama y configurar Build command y Publish directory con las rutas reales. Verificar el runtime si la construcción usa Python. Conservar el identificador del proyecto para actualizar el mismo sitio.

## Vercel

Importar el repositorio en la cuenta del usuario y seleccionar el framework correcto; para HTML estático sin framework, usar Other. Configurar el comando de construcción solo si corresponde y el directorio final. Si el constructor local necesita un runtime no disponible en el entorno de build, construir antes y desplegar la carpeta estática mediante la CLI oficial, vinculándola al proyecto correcto. No ejecutar el constructor específico de este visor sobre otro dashboard. Verificar la vista previa antes de promover a producción cuando el flujo lo permita.

## Verificación y migración

- Confirmar que el despliegue terminó correctamente y que la URL responde por HTTPS.
- Revisar index.html, CSS, JavaScript, imágenes, descargas, filtros y navegación; probar las rutas anidadas y la subruta base.
- Para recursos con manifiesto, comprobar integridad. La igualdad de archivos no sustituye la revisión funcional del navegador.
- Si hay protección, comprobar que el contenido protegido no se entrega en claro y que el usuario puede desbloquearlo sin compartir la clave con el agente.
- Registrar proveedor, propietario, repositorio, rama, proyecto, comando, carpeta de salida, URL, fecha, commit y cómo actualizar/recuperar. No registrar secretos.
- Al migrar, conservar la web anterior hasta verificar la nueva. Retirar su acceso público o despublicarla solo con autorización; no confundir hacerla privada con detener el hosting. No borrar el proyecto ni archivos.
- Entregar la URL y el estado real; si falta autenticación, dominio o una acción no disponible, indicar el paso exacto pendiente. No afirmar publicación solo por haber subido código a GitHub.

## Instrucción lista para pegar a Claude o Codex

> Lee AGENTS.md, README.md y 01 Docx/PUBLICAR_DASHBOARDS_MULTIPLATAFORMA.md. Quiero publicar este dashboard en mi propia cuenta. Identifica el constructor, la carpeta publicable y si necesita backend. Si no he elegido proveedor, preséntame GitHub Pages, Cloudflare Pages, Netlify, Vercel y servidor propio para escoger uno; si ya lo elegí, úsalo. Reutiliza el proyecto existente cuando corresponda. Prepara y verifica los archivos, conserva la protección de datos y no borres archivos ni guardes credenciales. Publica solo el contenido final autorizado. Documenta cómo actualizarlo y entrégame la URL verificada, el commit y cualquier pendiente concreto. No uses OpenAI Sites salvo que yo lo pida.

## Referencias oficiales

- [Fuentes de publicación de GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [HTML estático en Cloudflare Pages](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/)
- [Carga directa en Cloudflare Pages](https://developers.cloudflare.com/pages/get-started/direct-upload/)
- [Crear despliegues en Netlify](https://docs.netlify.com/deploy/create-deploys/)
- [Configurar builds en Vercel](https://vercel.com/docs/builds/configure-a-build)

Los agentes deben consultar estas referencias al ejecutar una publicación: los límites y las pantallas pueden cambiar.
