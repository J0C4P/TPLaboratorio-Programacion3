function crearCardCatalogo(producto){
  let imagen = "";
  if (producto.imagen !== "") {
    imagen = `<img src="${producto.imagen}" class="card-img-top" alt="${producto.nombre}">`;
  }
  return `<div class="col-12 col-md-6 col-lg-4">
    <article class="card h-100">
      ${imagen}
      <div class="card-body">
        <h3 class="card-title h5">${producto.nombre}</h3>
        <p class="card-text"><strong>Artesano:</strong> ${producto.creador} (${producto.localidad})</p>
        <p class="card-text"><strong>Categoría:</strong> ${producto.categoria}</p>
        <p class="card-text"><strong>Precio:</strong> $${producto.precio}</p>
        <p class="card-text"><strong>Descripción:</strong> ${producto.descripcion}</p>
        <p class="card-text"><strong>Stock:</strong> ${producto.stock}</p>
      </div>
    </article>
  </div>`;
}

function crearCardMisProductos(producto){
  return `<div class="col-12 col-md-6 col-lg-4">
    <article class="card h-100">
      <img src="${producto.imagen}" class="card-img-top" alt="${producto.nombre}">
      <div class="card-body">
        <h3 class="card-title h5">${producto.nombre}</h3>
        <p class="card-text"><strong>Categoría:</strong> ${producto.categoria}</p>
        <p class="card-text"><strong>Precio:</strong> $${producto.precio}</p>
        <p class="card-text"><strong>Descripción:</strong> ${producto.descripcion}</p>
        <p class="card-text"><strong>Stock:</strong> ${producto.stock}</p>
        <button onclick="eliminarProducto(${producto.id})">Eliminar</button>
        <button onclick="editarProducto(${producto.id})">Editar</button>
      </div>
    </article>
  </div>`;
}

function mostrarCatalogo(lista){
  let html = "";
  for (let producto of lista) {
    html += crearCardCatalogo(producto);
  }
  document.getElementById("listaCatalogo").innerHTML = html;
}
function mostrarMisProductos(lista){
  let html = "";
  for (let producto of lista) {
    html += crearCardMisProductos(producto);
  }
  document.getElementById("listaMisProductos").innerHTML = html;
}

document.addEventListener("DOMContentLoaded", function () {
  if (document.getElementById("listaCatalogo") !== null) {
    const catalogoGeneral = new Catalogo();
    for (let producto of misProductos.productos) {
      catalogoGeneral.agregarProducto(producto);
    }
    for (let producto of productosOtrosArtesanos.productos) {
      catalogoGeneral.agregarProducto(producto);
    }
    mostrarCatalogo(catalogoGeneral.productos);
  }
});
