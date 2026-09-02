# Poncho Digital

### La rama presente corresponde al avance de estilos del proyecto: CSS y Bootstrap

---
## Entrega – Estilos visuales: CSS y Bootstrap

En esta entrega se incorporaron estilos visuales al proyecto **Poncho Digital** a partir de hojas de estilo CSS propias y del framework Bootstrap 5. La estructura HTML de la entrega anterior se conserva y se complementa con una interfaz más consistente, responsive y orientada a la visualización del catálogo y los formularios.

### Páginas implementadas

- `Portada.html`: página principal con bienvenida, descripción del proyecto y navegación.
- `Formulario_artesano.html`: formulario para registrar la solicitud de participación de un artesano.
- `Mis_productos.html`: gestión visual de productos publicados por un artesano.

### Funcionalidades incluidas

- Navegación entre las páginas mediante enlaces `<a>`.
- Diseño compartido para encabezados, navegación, contenido principal y pie de página.
- Aplicación de una tipografía, paleta de colores y estilos generales propios del proyecto.
- Uso de Bootstrap 5 para navbar responsive, sistema de grilla, cards, formularios, botones y utilidades de espaciado.
- Adaptación responsive de las páginas para distintos tamaños de pantalla.
- Estilos específicos para el formulario de solicitud de participación de artesanos.
- Estilos específicos para el formulario de publicación y la gestión de productos.
- Estados visuales de validación y foco en los controles de los formularios.
- Formulario de solicitud de participación para artesanos.
- Formulario para publicar nuevos productos.
- Visualización de productos con nombre, imagen, categoría, precio, descripción y stock.
- Enlaces para modificar y eliminar publicaciones.
- Uso de etiquetas semánticas HTML5 como `header`, `nav`, `main`, `section`, `article` y `footer`.
- Controles de formulario acompañados por sus respectivas etiquetas `label`.
- Validaciones básicas mediante atributos HTML como `required`, `maxlength`, `min` y `max`.

### Recursos

Las imágenes de los productos se encuentran en la carpeta:

`Imagenes publicaciones/`

Bootstrap y la tipografía utilizada se incorporan mediante enlaces a CDN en las páginas HTML. Para utilizar correctamente estos recursos se necesita conexión a Internet al abrirlas.

Las hojas de estilo propias se encuentran en la carpeta `css/`:

- `Estilo_general.css`: estilos compartidos y estructura visual general.
- `Estilo_formulario.css`: estilos de formularios y controles.
- `Estilo_mis_productos.css`: estilos de la página de gestión de productos.
- `Estilo_Portada.css`: estilos específicos de la página principal.

### Estado del proyecto

Esta rama corresponde a la etapa de incorporación de estilos, enfocada en mejorar la presentación, la consistencia visual y la adaptación responsive de las páginas HTML. La lógica de negocio y la integración con Django y PostgreSQL permanecen pendientes.
---

Plataforma digital de Artesanos de la Fiesta Nacional e Internacional del Poncho.
 
Trabajo de Laboratorio 2026 — Cátedra Programación III — Facultad de Tecnología y Ciencias Aplicadas (FTyCA), Universidad Nacional de Catamarca (UNCa).
 
## Integrantes del equipo
 
| Nombre y Apellido | Matrícula | GitHub |
|---|---|---|
| Capdevila José | 01728 | J0C4P |
| Vega Lourdes | 01767 | Lourdes-Vega |
| Augusto Trainer | 01715 | Augusto-H4u |
 
## Instalación y configuración
 
Por el momento, el proyecto puede visualizarse abriendo `html/Portada.html` en un navegador. Las páginas cargan Bootstrap y la tipografía desde CDN, por lo que se requiere conexión a Internet para disponer de todos los estilos.
 
## Tecnologías
 
- Framework: Django
- Base de datos: PostgreSQL
- Frontend: HTML5, CSS3, Bootstrap, JavaScript