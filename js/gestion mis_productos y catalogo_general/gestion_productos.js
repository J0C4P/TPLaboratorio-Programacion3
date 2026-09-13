function producto(id_producto, id_artesano, nombre_producto, categoria, precio, descripcion, localidad, ubicacion_stand, artesano, url_imagen) {
    this.id_producto = id_producto;
    this.id_artesano = id_artesano;
    this.nombre_producto = nombre_producto;
    this.categoria = categoria;
    this.precio = precio;
    this.descripcion = descripcion;
    this.localidad = localidad;
    this.ubicacion_stand = ubicacion_stand;
    this.artesano = artesano;
    this.url_imagen = url_imagen;
}

class catalogo{
    constructor() {
        this.productos = [];
    }
    agregarProductos(...productos){
        let producto;
        productos.forEach((producto) =>{
            this.productos.push(producto);
        })
    };
}

let producto1 = new producto(1, 1, "Poncho tejido", "Textil", "$450.000", "Poncho artesanal de fibra regional hecho a telar.", "Belén", 'Pabellón "Artesanias" - Stand 14', "Jose Luis Esparramo", "../Imagenes%20publicaciones/Poncho_SanMartin_artesano1.jpg");
let producto2 = new producto(2, 1, "Manta de lana de vicuña", "Textil", "$250.000", "Pieza fina hilada a mano en telar criollo, sin tintes químicos.", "Belén", 'Pabellón "Artesanias" - Stand 14', "Jose Luis Esparramo", "../Imagenes%20publicaciones/manta_lana_artesano1.jpg");
let producto3 = new producto(3, 1, "Ruana en fibra de llama", "Textil", "$87.000", "Ruana abrigo unisex con acabado desflecado a mano.", "Belén", 'Pabellón "Artesanias" - Stand 14', "Jose Luis Esparramo", "../Imagenes%20publicaciones/Ruana_fibra_artesano1.jpg");
let producto4 = new producto(4, 1, "Botellón cerámico de Arcilla roja", "Cerámica", "$42.000", "Pieza modelada en arcilla roja con engobes minerales y pulido a piedra.", "Santa María", 'Pabellón "Artesanias" - Stand 14', "Jose Luis Esparramo", "../Imagenes%20publicaciones/Botellon_ceramico_arcRoja_artesano1.jpg");
let producto5 = new producto(5, 1, "Juego de cuencos (Set x4)", "Cerámica", "$70.000", "Set de cuencos utilitarios horneados a leña, aptos para alimentos.", "Santa María", 'Pabellón "Artesanias" - Stand 14', "Jose Luis Esparramo", "../Imagenes%20publicaciones/Juego_cuencos_artesano1.jpg");
let producto6 = new producto(6, 1, "Colgante de Rodocrosita", "Orfebrería y Joyería", "$500.000", "Colgante gota con piedra Rosa del Inca tallada y engarzada en plata.", "Andalgalá", 'Pabellón "Artesanias" - Stand 14', "Jose Luis Esparramo", "../Imagenes%20publicaciones/Colgante_rodocrosita_artesano1.jpg");
let producto7 = new producto(7, 1, "Cuchillo artesanal de guampa", "Orfebrería y Joyería", "$90.000", "Hoja de acero al carbono forjada a mano con cabo en guampa y madera.", "Tinogasta", 'Pabellón "Artesanias" - Stand 14', "Jose Luis Esparramo", "../Imagenes%20publicaciones/Cuchillo_guampa_artesano1.jpg");
let producto8 = new producto(8, 1, "Dulce de cayote", "Gastronomía Regional", "$15.000", "Dulce en hebras cocinado en paila de cobre sin conservantes.", "San Fernando del Valle", 'Pabellón "Artesanias" - Stand 14', "Jose Luis Esparramo", "../Imagenes%20publicaciones/Dulce_cayote_artesano1.jpg");

let Catalogo = new catalogo();

Catalogo.agregarProductos(producto2, producto4, producto1, producto6, producto3, producto5, producto8, producto7);

document.addEventListener("DOMContentLoaded", () => {
    let galeria = document.getElementById("galeria_general");

    Catalogo.productos.forEach( producto => {
        let li_producto = document.createElement("li");
        li_producto.className = "col-12 col-md-6 col-lg-4 mb-2";

        li_producto.innerHTML = `<article class="card h-100">
                                <img src="${producto.url_imagen}" class="card-img-top" width="300" height="300" alt="${producto.nombre_producto}">
                                <div class="card-body">
                                    <div class="d-flex justify-content-between align-items-start">
                                        <h3 class="card-title h5 mb-3">${producto.nombre_producto}</h3>
                                        <button type="button" class="boton_fav" title="Agregar a favoritos">☆</button>
                                    </div>
                                    <p class="card-text mb-2 categoria-art"><strong>Categoría:</strong> ${producto.categoria}</p>
                                    <p class="card-text mb-2"><strong>Precio:</strong> ${producto.precio}</p>
                                    <p class="card-text mb-2"><strong>Descripción:</strong> ${producto.descripcion}</p>
                                    <p class="card-text mb-2 localidad-art"><strong>Localidad:</strong> ${producto.localidad}</p>
                                    <p class="card-text mb-3"><strong>Ubicación del puesto:</strong> ${producto.ubicacion_stand}</p>
                                    <p class="card-text mb-3"><strong>Artesano:</strong> ${producto.artesano}</p>

                                    <a href="#" class="btn btn-outline-secondary btn-sm flex-fill">Ver artesano</a>
                                    <a href="#" class="btn btn-outline-primary btn-sm flex-fill">Ver en mapa</a>
                                </div>
                            </article>`

        galeria.appendChild(li_producto);

    })
});

