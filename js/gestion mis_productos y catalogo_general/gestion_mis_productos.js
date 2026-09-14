
let articulos = document.getElementById("galeria_general");

//Nuevo producto
document.addEventListener("DOMContentLoaded", () =>{
    let formulario = document.getElementById("formulario");

    formulario.addEventListener("submit", (event) =>{
        event.preventDefault(); //antes de enviar se pierda info

        let datos = new FormData(formulario);

        let nuevo_art = document.createElement("li");
        nuevo_art.className = "col-12 col-md-6 col-lg-4 mb-2";

        let archivo = datos.get('imagen_pub');
        let ruta_temporal_imagen = URL.createObjectURL(archivo);

        nuevo_art.innerHTML = `<article class="card h-100">
                                <img src="${ruta_temporal_imagen}" class="card-img-top" width="300" height="300" alt="${datos.get('nom_publicacion')}" >

                                <div class="card-body">
                                    <h3 class="card-title h5 mb-3">${datos.get('nom_publicacion')}</h3>
                                    <p class="card-text mb-3"><strong>Categoría:</strong> ${datos.get('categoria')}</p>
                                    <p class="card-text mb-3"><strong>Precio:</strong> ${datos.get('precio')}</p>
                                    <p class="card-text mb-3"><strong>Descripción:</strong> ${datos.get('descripcion')}</p>
                                    <p class="card-text mb-3"><strong>Stock disponible:</strong> ${datos.get('stock')}</p>

                                    <a href="modificar_producto.html" target="_blank" class="btn btn-outline-primary btn-sm">Modificar</a>
                                    <a href="eliminar_publicacion.html" target="_blank" class="btn btn-outline-danger btn-sm">Eliminar publicacion</a>
                                </div>
                            </article>`

        articulos.appendChild(nuevo_art);

        formulario.reset();
    });
});

// Eliminar articulo
document.addEventListener("DOMContentLoaded", () =>{
    articulos.querySelectorAll("li").forEach(articulo =>{
        let btn_eliminar = articulo.getElementsByClassName("btn-eliminar")[0];

        btn_eliminar.addEventListener("click", () =>{
            if(confirm("¿Esta seguro que desea eliminar dicho articulo?")){
                articulo.remove();
            }
        })
    })
});


// Modificar articulo
document.addEventListener("DOMContentLoaded", () => {
    articulos.querySelectorAll("li").forEach(articulo =>{
        let btn_modificar = articulo.querySelector("button.btn-modificar");

        btn_modificar.addEventListener("click", () =>{

            if(articulo.querySelector("form")){
                return;
            }

            let nombre = articulo.querySelector("h3").textContent.trim();
            let precio = articulo.querySelectorAll("p")[1].textContent.replace("Precio: $", "").trim();
            let descripcion = articulo.querySelectorAll("p")[2].textContent.replace("Descripción: ", "").trim();
            let stock = articulo.querySelectorAll("p")[3].textContent.replace("Stock disponible: ", "").replace("unidades", "").trim();

            let formulario_temporal = document.createElement("form");
            formulario_temporal.className = "border-top pt-3 mt-3 bg-light p-2 rounded"
            formulario_temporal.innerHTML = `
                            <ul class="row">
                                <li class="col-12">
                                    <label for="publicacion" class="form-label">Nombre: </label>
                                    <input type="text" name="nom_publicacion" class="form-control" id="publicacion" value= "${nombre}" required>
                                </li>

                                <li class="col-12">
                                    <label for="precio" class="form-label">Precio (sin $): </label>
                                    <input type="number" name="precio" class="form-control" id="precio" value="${precio}" required>
                                </li>

                                <li class="col-12">
                                    <label for="desc" class="form-label">Descripcion del Producto: </label>
                                    <textarea name="descripcion" class="form-control" id="desc" rows="2" required>${descripcion}</textarea>
                                </li>

                                <li class="col-12">
                                    <label for="stock" class="form-label">Stock disponible: </label>
                                    <input type="number" name="stock" class="form-control" id="stock" value="${stock}" required>
                                </li>
                                <div class="d-flex gap-2 mt-2">
                                    <button type="submit" class="btn btn-success btn-sm flex-fill">Guardar</button>
                                    <button type="reset" class="btn btn-secondary btn-sm btn-cancelar flex-fill">Cancelar</button>
                                </div>`
            articulo.querySelector(".card-body").append(formulario_temporal);

            formulario_temporal.addEventListener("reset", ()=>{
                formulario_temporal.remove();
            })

            formulario_temporal.addEventListener("submit", (event) =>{
                event.preventDefault();

                let datos_nuevos = new FormData(formulario_temporal);

                let nombre_nuevo = datos_nuevos.get("nom_publicacion");
                let precio_nuevo = datos_nuevos.get("precio");
                let descripcion_nueva = datos_nuevos.get("descripcion");
                let stock_nuevo = datos_nuevos.get("stock");

                articulo.querySelector("h3").innerHTML = `${nombre_nuevo}`;
                articulo.querySelectorAll("p")[1].innerHTML = `<strong>Precio:</strong> $${precio_nuevo}`;
                articulo.querySelectorAll("p")[2].innerHTML = `<strong>Descripción:</strong> ${descripcion_nueva}`;
                articulo.querySelectorAll("p")[3].innerHTML = `<strong>Stock disponible:</strong> ${stock_nuevo} unidades`;

                formulario_temporal.remove();
            });
        })
    })
})