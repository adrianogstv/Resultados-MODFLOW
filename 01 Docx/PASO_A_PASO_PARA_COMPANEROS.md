# Publicar y compartir tu dashboard: paso a paso

Para compañeros que empiezan desde cero. Revisado: 17/11/2026.

## 1. Decide qué quieres compartir

Un dashboard HTML con CSS, JavaScript y datos exportados puede publicarse como web estática. Sus filtros y gráficos funcionan en el navegador, sin mantener tu computadora encendida. GitHub Pages no ejecuta Python, Streamlit, Dash, Flask ni bases de datos: si tu aplicación necesita uno de esos servidores, utiliza un alojamiento con backend. Puedes exportar un informe estático cuando tu herramienta lo permita.

Este repositorio contiene dos cosas: un visor WPC real y documentación reutilizable. Para tu dashboard, crea tu propio repositorio; no copies los resultados WPC como si fueran datos de ejemplo. Para escoger otro proveedor, consulta [la guía multiplataforma](PUBLICAR_DASHBOARDS_MULTIPLATAFORMA.md).

## 2. Prepara tus archivos

Utiliza esta estructura, adaptada a las convenciones de tu proyecto:

```text
00 Code/visor/index.html
00 Code/visor/app.js
00 Code/visor/app.css
01 Docx/
02 Input/
03 Output/
```

El punto de entrada debe llamarse index.html. Cada archivo necesario debe acompañarlo o tener una URL accesible. Cambia rutas como C:/datos/tabla.csv por rutas web relativas; revisa mayúsculas y minúsculas. Abre la carpeta con un servidor local para probar fetch y las descargas; abrir HTML con doble clic no reproduce todas las condiciones de una web.

No incluyas archivos privados, credenciales ni modelos nativos innecesarios. Un repositorio público y los recursos de una web pública son descargables. Una pantalla de contraseña por sí sola no protege archivos en claro. Usa cifrado real o un servicio con autenticación cuando corresponda.

## 3. Crea el repositorio en tu cuenta

1. Inicia sesión en GitHub y crea un repositorio para ese dashboard, por ejemplo dashboard-cuenca.
2. Con GitHub Free, la ruta habitual para Pages es un repositorio público. Antes de subir nada, revisa si puedes divulgar el código y los datos.
3. Clona el repositorio con Git o GitHub Desktop, agrega tus archivos y confirma los cambios mediante un commit. Sube los cambios con push.
4. Si prefieres cargar archivos en el navegador, respeta su límite por archivo. Para archivos grandes usa Git y revisa los límites de la sección 9.

No uses este repositorio de resultados para almacenar todos los proyectos de la empresa. Un repositorio por dashboard facilita permisos, historial y mantenimiento.

## 4. Configura la publicación automática

En tu repositorio, abre Settings → Pages y selecciona GitHub Actions como fuente. Para un dashboard HTML simple cuyo contenido publicable completo está en 00 Code/visor, crea .github/workflows/publicar-pages.yml con este contenido:

```yaml
name: Publicar dashboard
on:
  push:
    branches: [main]
    paths:
      - '00 Code/visor/**'
      - '.github/workflows/publicar-pages.yml'
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
      - uses: actions/checkout@v6
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v4
        with:
          path: '00 Code/visor'
      - id: deployment
        uses: actions/deploy-pages@v4
```

Este ejemplo sirve únicamente cuando esa carpeta YA contiene todos los archivos publicables. No incorpora por sí solo datos de 02 Input ni compila frameworks. Si necesitas construir, agrega antes de upload una etapa con tu comando real y cambia path por la carpeta final, por ejemplo 03 Output/PAGES/dist. Agrega también las entradas necesarias al filtro paths para que sus cambios disparen el flujo. Para Vite, React u otra herramienta, identifica su constructor y configura su ruta base para la subruta del repositorio.

En el visor WPC de este repositorio NO reemplaces el workflow existente: ya reconstruye y verifica los recursos cifrados. Sigue [su guía específica](PUBLICAR_DESDE_GITHUB.md).

## 5. Espera el despliegue y revisa

1. Confirma y sube el workflow junto con los archivos.
2. Abre Actions y entra en Publicar dashboard. Si no arrancó por el filtro de rutas, utiliza Run workflow.
3. Espera a que termine correctamente; si falla, abre la etapa que aparece en rojo y corrige la causa.
4. Copia la URL del despliegue. Normalmente será https://TU_USUARIO.github.io/TU_REPOSITORIO/ . No inventes la URL: usa la que devuelve GitHub.
5. Prueba filtros, imágenes, descargas y navegación. Revisa también desde una ventana privada o con un compañero para detectar permisos o recursos locales que faltan.

Subir código a GitHub no significa que la web ya esté publicada. Debe existir un despliegue exitoso y una URL funcional.

## 6. Comparte y actualiza

Comparte la URL de la web. Los visitantes de una web pública no necesitan clonar el repositorio. Para colaborar en el código, agrega colaboradores desde los permisos del repositorio, con los roles necesarios.

Para actualizar, edita los archivos, revisa localmente, crea un commit y haz push a main. El workflow vuelve a publicar cuando cambian las rutas configuradas. Tus compañeros conservan el mismo enlace. No hace falta volver a crear el sitio. Espera el despliegue antes de anunciar la actualización; si ves una versión antigua, recarga y comprueba caché y commit.

## 7. Qué significa «en tiempo real»

| Necesidad | Solución | Qué debes saber |
|---|---|---|
| Ver cambios al subir una nueva versión | Despliegue automático por push | Hay demora de construcción y despliegue; no es instantáneo |
| Mostrar nuevos CSV o resultados cada día | Un proceso obtiene datos, exporta y publica | Debe ejecutar en un servidor o CI; no depende de una PC apagada |
| Consultar datos actuales cada minuto | El navegador consulta una API autorizada | La API necesita HTTPS, permisos CORS, límites y control de acceso; las claves privadas quedan en backend |
| Compartir filtros y ediciones entre usuarios | Backend/base de datos y, si aplica, WebSockets | Pages solo aloja el frontend; no sincroniza sesiones ni guarda cambios compartidos |

GitHub Actions permite tareas programadas, pero sus horarios pueden demorarse y no garantizan ejecución al segundo. No uses commits y despliegues continuos como una base de datos en tiempo real. Si necesitas datos en vivo, sirve los datos mediante una API y muestra fecha/hora de actualización, estado de conexión y datos antiguos cuando falle. Que todos abran el mismo enlace no sincroniza automáticamente sus filtros.

## 8. Antes de publicar datos de trabajo

Confirma con el responsable qué datos pueden ser públicos. Un repositorio privado no implica automáticamente que Pages sea privado: las opciones de acceso dependen del plan. No guardes tokens en el código del navegador. Los datos cifrados siguen ocupando espacio y consumiendo tráfico; el cifrado protege contenido, no reduce su tamaño. Revisa los términos de uso si el dashboard es un servicio comercial: Pages no está destinado a operar negocios en línea, comercio electrónico o SaaS comercial.

## 9. Límites de GitHub y Pages

No es un límite de unos pocos KB. Son restricciones distintas, verificadas en documentación oficial el 17/11/2026:

| Concepto | Límite o recomendación |
|---|---|
| Cargar un archivo mediante el navegador de GitHub | Hasta 25 MiB por archivo |
| Archivo en Git normal | Advertencia sobre 50 MiB; bloqueo sobre 100 MiB |
| Repositorio en general | Idealmente menor de 1 GB; fuertemente recomendado menor de 5 GB |
| Repositorio fuente de Pages | Recomendado hasta 1 GB |
| Sitio publicado en Pages | Máximo 1 GB |
| Tráfico de Pages | Límite flexible de 100 GB/mes |
| Despliegue de Pages | Timeout si supera 10 minutos |
| Builds de Pages | Límite flexible de 10/h; no aplica al workflow personalizado de Actions |

Fuentes: [archivos y repositorios](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) y [Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits). MiB equivale a 1.048.576 bytes; GB y MiB no son unidades idénticas. Los límites de Git normal no deben confundirse con límites de artefactos de despliegue.

Git LFS tiene condiciones y cuotas propias y no debe asumirse como solución para servir recursos de Pages; comprobar compatibilidad antes de adoptarlo. Tampoco fracciones un archivo pesado para eludir el límite total del sitio. Para datasets, videos o resultados masivos, usa almacenamiento de objetos o un servicio apropiado, con permisos y presupuesto revisados. Las versiones históricas de archivos grandes siguen aumentando el repositorio aunque una nueva versión pese menos.

Ejemplo orientativo: si cada visita descarga 20 MB, 5.000 visitas representan aproximadamente 100 GB, sin considerar caché ni otras solicitudes. Optimiza imágenes, evita cargar todos los GIF de entrada y descarga datos bajo demanda. La velocidad de apertura suele ser un problema antes de llegar al máximo de almacenamiento.

Actions tiene sus propias cuotas de ejecución, almacenamiento y artefactos según plan, repositorio y runner; el límite de builds de Pages no elimina estas cuotas. Revisa [facturación de Actions](https://docs.github.com/en/billing/concepts/product-billing/github-actions) antes de automatizar tareas frecuentes. No activar pagos adicionales sin autorización.

## 10. Resolver problemas frecuentes

| Problema | Revisión |
|---|---|
| 404 | Deployment exitoso, Pages habilitado e index.html en raíz del artefacto |
| Página sin estilo o sin datos | Rutas relativas, mayúsculas, subruta base y errores de red del navegador |
| Cambios no aparecen | Filtro paths, rama main, workflow, commit desplegado y caché |
| Error de permisos al publicar | pages: write, id-token: write y entorno github-pages |
| Funciona solo en mi PC | Rutas de disco, archivos faltantes, servidor/API local |
| Archivo rechazado | Método de subida, tamaño individual y políticas de GitHub |
| Necesita ejecutar Python por cada visitante | Elegir backend; no intentar ejecutarlo en Pages |

## 11. Instrucción para un agente

> Lee AGENTS.md y esta guía. Ayúdame a publicar MI dashboard en MI cuenta. Confirma si es estático o necesita backend; si no he elegido alojamiento, presenta las opciones de la guía multiplataforma. Reutiliza el proyecto correcto, prepara únicamente la carpeta publicable y configura actualizaciones automáticas. Revisa tamaños, privacidad y rutas. No copies resultados WPC a mi dashboard, no borres archivos, no publiques secretos y no actives pagos sin autorización. Verifica despliegue y funciones, entrega el enlace y documenta cómo actualizarlo. Si pido tiempo real, distingue despliegue por cambios de datos vivos y propón la arquitectura correspondiente.
