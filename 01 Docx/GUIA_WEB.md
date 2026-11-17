# Código de la web WPC KCB

Repositorio: https://github.com/adrianogstv/Resultados-MODFLOW

Web actual: https://wpc-kcb-evaluaciones-cifradas.saltymars15.chatgpt.site/

Para los pasos de publicación, el texto listo para usar en Codex y la alternativa de GitHub Pages, consultar [Publicar desde GitHub](PUBLICAR_DESDE_GITHUB.md).

## Qué se conserva aquí

Una copia del frontend y de todos los recursos cifrados de la publicación existente, con hashes de integridad. No es una regeneración científica ni una actualización con las entregas locales posteriores. Se conserva el catálogo publicado, incluidas sus limitaciones numéricas.

- **00 Code/visor**: HTML, CSS y JavaScript del visor.
- **00 Code/herramientas**: reconstrucción verificable de la publicación.
- **01 Docx**: documentación de operación.
- **02 Input/publicacion**: parámetros públicos de cifrado y manifiesto de integridad.
- **02 Input/recursos_cifrados**:34 partes de un ZIP que contiene únicamente el catálogo y archivos cifrados. Cada parte pesa como máximo3MiB.
- **03 Output**: destino local de reconstrucciones; ignorado por Git.

Los recursos conservan AES-GCM256 y PBKDF2-SHA256. La contraseña y la clave derivada no se guardan en el repositorio. El navegador deriva la clave cuando el visitante introduce su contraseña. `crypto.json` contiene sal y parámetros públicos, no una credencial.

Los archivos nativos MODFLOW y los originales de figuras/tablas sin cifrar permanecen fuera de este repositorio. La división en partes facilita versionar los datos cifrados; no es una protección adicional al cifrado existente.

## Reconstruir

Requiere Python3.9 o posterior, solo biblioteca estándar. Desde la raíz del repositorio:

```powershell
python -B "00 Code/herramientas/preparar_publicacion.py"
```

El comando crea una carpeta nueva en03 Output. Dentro quedan el ZIP cifrado ensamblado, `dist/`, la configuración `.openai/hosting.json` y una verificación. No se borran archivos ni se sobrescriben versiones anteriores. Se comprueban840 archivos y sus hashes.

Para probar la carpeta dist generada:

```powershell
python -m http.server 8000 --directory "03 Output/PUBLICACION_FECHA_HORA/dist"
```

Abrir http://localhost:8000. El cifrado web requiere localhost o HTTPS; abrir index.html con file:// no es equivalente. La contraseña se introduce solamente en el visor. No escribirla en código, README, commits, variables públicas ni workflows.

## GitHub y Sites son pasos distintos

GitHub conserva el código y el historial. Sites mantiene el enlace publicado. Este repositorio no activa una publicación automática, no cambia la audiencia y no habilita GitHub Pages. Para actualizar Sites se reconstruye una nueva carpeta de publicación, se revisa y se usa el flujo de publicación conservando el project_id del Site existente. Las credenciales de publicación se gestionan fuera de Git.

Los cuatro archivos de aplicación/cifrado/catálogo se cotejaron con la web viva el17/11/2026. El HTML original conserva la interfaz sin los scripts que la plataforma puede añadir al servirlo. La reconstrucción conserva los bytes del frontend de origen y de los recursos cifrados.

## Actualizar resultados en el futuro

La generación de nuevos resultados y su cifrado se realiza fuera de este repositorio, sobre un conjunto aprobado de figuras. Incorporar después el nuevo frontend, manifiesto y partes cifradas con revisión de secretos y trazabilidad. No incorporar modelos o resultados descifrados para simplificar la actualización. La copia aquí preservada es la publicación existente, no las carpetas de objetivos de calibración ni la última entrega local completa.
