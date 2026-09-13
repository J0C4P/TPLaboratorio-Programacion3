class Catalogo{
  constructor(){
    this.productos = [];
  }

  agregarProducto(producto){
    this.productos.push(producto);
  }
  eliminarProducto(id){
    this.productos = this.productos.filter(producto => producto.id !== id);
  }
}

/*Mis productos*/
const misProductos = new Catalogo();

misProductos.agregarProducto(new Producto(
  1, "Poncho tejido", "Poncho artesanal de fibra regional hecho a telar.",
  "Textil", 450000, 3, "../Imagenes%20publicaciones/Poncho_SanMartin_artesano1.jpg",
  "Artesano 0", "Belén", false
));
misProductos.agregarProducto(new Producto(
  2, "Manta de lana de vicuña", "Pieza fina hilada a mano en telar criollo, sin tintes químicos.",
  "Textil", 250000, 1, "../Imagenes%20publicaciones/manta_lana_artesano1.jpg",
  "Artesano 0", "Belén", false
));
misProductos.agregarProducto(new Producto(
  3, "Ruana en fibra de llama", "Ruana abrigo unisex con acabado desflecado a mano.",
  "Textil", 87000, 5, "../Imagenes%20publicaciones/Ruana_fibra_artesano1.jpg",
  "Artesano 0", "Belén", false
));
misProductos.agregarProducto(new Producto(
  4, "Botellón cerámico de Arcilla roja", "Pieza modelada en arcilla roja con engobes minerales y pulido a piedra.",
  "Cerámica", 42000, 4, "../Imagenes%20publicaciones/Botellon_ceramico_arcRoja_artesano1.jpg",
  "Artesano 0", "Belén", false
));
misProductos.agregarProducto(new Producto(
  5, "Juego de cuencos (Set x4)", "Set de cuencos utilitarios horneados a leña, aptos para alimentos.",
  "Cerámica", 70000, 10, "../Imagenes%20publicaciones/Juego_cuencos_artesano1.jpg",
  "Artesano 0", "Belén", false
));
misProductos.agregarProducto(new Producto(
  6, "Colgante de Rodocrosita", "Colgante gota con piedra Rosa del Inca tallada y engarzada en plata.",
  "Orfebrería y Joyería", 500000, 5, "../Imagenes%20publicaciones/Colgante_rodocrosita_artesano1.jpg",
  "Artesano 0", "Belén", false
));
misProductos.agregarProducto(new Producto(
  7, "Cuchillo artesanal de guampa", "Hoja de acero al carbono forjada a mano con cabo en guampa y madera.",
  "Orfebrería y Joyería", 90000, 6, "../Imagenes%20publicaciones/Cuchillo_guampa_artesano1.jpg",
  "Artesano 0", "Belén", false
));
misProductos.agregarProducto(new Producto(
  8, "Dulce de cayote", "Dulce en hebras cocinado en paila de cobre sin conservantes.",
  "Gastronomía Regional", 15000, 35, "../Imagenes%20publicaciones/Dulce_cayote_artesano1.jpg",
  "Artesano 0", "Belén", false
));

/*Productos de otros artesanos*/
const productosOtrosArtesanos = new Catalogo();

productosOtrosArtesanos.agregarProducto(new Producto(
  9, "Poncho de vicuña", "Poncho tejido en telar criollo con fibra de vicuña de la Puna.",
  "Textil", 1200000, 1, "", "Artesano 2", "Belén", false
));
productosOtrosArtesanos.agregarProducto(new Producto(
  10, "Tapiz con guardas andinas", "Tapiz de lana de oveja teñido con tintes naturales.",
  "Textil", 95000, 4, "", "Artesano 2", "Belén", false
));
productosOtrosArtesanos.agregarProducto(new Producto(
  11, "Vasija de cerámica negra", "Vasija modelada a mano y cocida en horno a leña.",
  "Cerámica", 38000, 7, "", "Artesano 3", "Santa María", false
));
productosOtrosArtesanos.agregarProducto(new Producto(
  12, "Aros de plata y rodocrosita", "Aros de plata 925 con rodocrosita de Capillitas.",
  "Orfebrería y Joyería", 65000, 12, "", "Artesano 4", "Andalgalá", false
));
productosOtrosArtesanos.agregarProducto(new Producto(
  13, "Vino patero artesanal", "Botella de vino patero elaborado de forma tradicional en Fiambalá.",
  "Gastronomía Regional", 12000, 24, "", "Artesano 5", "Tinogasta", false
));
productosOtrosArtesanos.agregarProducto(new Producto(
  14, "Nueces confitadas", "Frasco de nueces catamarqueñas confitadas en almíbar.",
  "Gastronomía Regional", 9000, 20, "", "Artesano 6", "San Fernando del Valle", false
));