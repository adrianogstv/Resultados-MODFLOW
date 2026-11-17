# Publicación del visor

- Alojamiento vigente: GitHub Pages, https://adrianogstv.github.io/Resultados-MODFLOW/.
- Flujo: .github/workflows/publicar-pages.yml. Publicar por push a main de código/recursos o manualmente desde Actions.
- No usar Sites ni crear un Site nuevo. .openai/hosting.json es un archivo histórico archivado, no configuración activa.
- Orden:00 Code,01 Docx,02 Input,03 Output. No borrar ni mover archivos.
- Conservar cifrado y no guardar contraseñas, claves ni modelos nativos en Git.
- El constructor debe validar los840 archivos y generar solo la web bajo dist; publicar únicamente ese directorio.
- Las modificaciones documentales no disparan el despliegue automático. Tras cambios de código/recursos, comprobar Actions y la URL pública.

## Publicación reutilizable
- Para compañeros nuevos y solicitudes de tiempo real, leer primero 01 Docx/PASO_A_PASO_PARA_COMPANEROS.md: distingue despliegue automático de datos vivos y documenta límites oficiales.
- La eliminación expresamente autorizada se limita al sitio antiguo identificado en 01 Docx/RETIRAR_SITIO_ANTIGUO_OPENAI.md. Los archivos locales y GitHub se conservan. No informar eliminación sin evidencia.
- Para elegir alojamiento de otros dashboards, leer 01 Docx/PUBLICAR_DASHBOARDS_MULTIPLATAFORMA.md. Preguntar el proveedor solo si no está decidido; usar cuentas del usuario y no OpenAI Sites por defecto.
- La elección de otro destino para otro dashboard no autoriza cambiar el alojamiento vigente de este visor.
