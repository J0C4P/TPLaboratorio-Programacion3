document.addEventListener("DOMContentLoaded", () => {
let elem_filtro_categoria = document.getElementById("filtro_categoria");
let elem_filtro_localidad = document.getElementById("filtro_localidad");

    elem_filtro_categoria.addEventListener("change", filtrado);
    elem_filtro_localidad.addEventListener("change", filtrado);

    function filtrado() {
        let articulos = document.querySelectorAll("#galeria_general li");
        let valor_categoria_filtro = `Categoría: ${elem_filtro_categoria.value}`;
        let valor_localidad_filtro = `Localidad: ${elem_filtro_localidad.value}`;

        articulos.forEach(articulo => {
            let valor_categoria_elemento = articulo.querySelector("p.categoria-art").textContent;
            let valor_localidad_elemento = articulo.querySelector("p.localidad-art").textContent;

            if ((valor_categoria_elemento === valor_categoria_filtro || valor_categoria_filtro === "Categoría: Todos los rubros")
                && (valor_localidad_elemento === valor_localidad_filtro || valor_localidad_filtro === "Localidad: Todas las localidades"))
            {
                articulo.style.display = "block"; //si coincide no lo borra de pantalla
            }
            else {
                articulo.style.display = "none"; //si no coincide, lo elimina de pantalla
            }
        });
    }
});
