# Poncho Digital

### Rama actual: JavaScript (Frontend dinámico)

---

## Descripción general

Esta rama corresponde al avance del proyecto **Poncho Digital** centrado en la lógica del frontend con **JavaScript**. Se trabaja sobre una versión estática del sitio, con HTML, CSS y Bootstrap, pero incorporando comportamiento dinámico para catalogar productos, aplicar filtros, buscar, guardar favoritos y gestionar publicaciones.

El proyecto sigue orientado a una plataforma digital para la **Fiesta Nacional e Internacional del Poncho**, con foco en la exhibición de productos artesanales y la postulación de artesanos.

---

## Páginas principales

- `html/Portada.html`: portada con información general del evento, navegación y presentación del proyecto.
- `html/Catalogo_general.html`: catálogo con listado de productos, filtros por categoría y localidad, barra de búsqueda y favoritos.
- `html/Mis_productos.html`: sección de gestión de productos del artesano con carga y edición de publicaciones.
- `html/Formulario_artesano.html`: formulario de inscripción para artesanos.

---

## Funcionalidades implementadas en esta rama

- Carga dinámica de productos desde JavaScript.
- Renderizado del catálogo en la interfaz sin necesidad de un backend.
- Filtro por categoría y localidad.
- Buscador de productos por nombre o contenido relevante.
- Sistema de favoritos con almacenamiento en el navegador.
- Visualización de productos con imagen, precio, descripción, categoría, localidad y puesto.
- Formulario para agregar nuevas publicaciones al catálogo.
- Edición y eliminación visual de publicaciones dentro de la gestión de productos.
- Validaciones de formularios con JavaScript.
- Comentarios con validación de longitud mínima.
- Diseño responsive con Bootstrap y CSS propio.

---

## Estructura del proyecto

- `css/`: estilos generales del sitio.
- `html/`: archivos HTML de cada vista.
- `js/`: scripts de comportamiento.
  - `formulario_artesano.js`: validaciones del formulario de artesano.
  - `validaciones.js`: validaciones generales.
  - `portada/portada.js`: comportamiento de la portada.
  - `gestion mis_productos y catalogo_general/`: lógica del catálogo, búsqueda, filtros, favoritos y gestión de productos.
- `Imagenes publicaciones/`: imágenes de los productos.
- `Imagenes-portada/`: imágenes de la portada.

---

## Tecnologías utilizadas

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

> En esta etapa del proyecto no hay integración con backend, base de datos ni servidor de aplicación. La funcionalidad se ejecuta en el navegador y simula la lógica de negocio del frontend.

---

## Instalación y uso

1. Clonar o abrir el repositorio en el editor.
2. Abrir cualquiera de los archivos HTML dentro de la carpeta `html/` en un navegador.
3. Para visualizar mejor la navegación, se recomienda abrir `html/Portada.html` como punto de inicio.
4. Si se desea probar funciones dinámicas del frontend, se puede abrir la aplicación directamente desde el navegador sin necesidad de un servidor local.

> Debido a que el proyecto usa Bootstrap y recursos externos desde CDN, es conveniente contar con conexión a Internet para cargar correctamente los estilos.

---

## Integrantes del equipo

| Nombre y Apellido | Matrícula | GitHub |
|---|---|---|
| Capdevila José | 01728 | J0C4P |
| Vega Lourdes | 01767 | Lourdes-Vega |
| Augusto Trainer | 01715 | Augusto-H4u |

---

## Estado del proyecto

La rama actual corresponde a la etapa de implementación del comportamiento del frontend con JavaScript. El proyecto ya cuenta con una base visual y funcional del catálogo y la gestión de productos, pero aún no incluye integración con backend, persistencia real de datos ni base de datos.

Trabajo de Laboratorio 2026 — Cátedra Programación III — Facultad de Tecnología y Ciencias Aplicadas (FTyCA), Universidad Nacional de Catamarca (UNCa).