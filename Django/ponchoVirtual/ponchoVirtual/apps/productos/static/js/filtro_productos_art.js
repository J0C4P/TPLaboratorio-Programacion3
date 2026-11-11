document.addEventListener("DOMContentLoaded", () => {
    let elem_filtro_categoria = document.getElementById("filtro_categoria");

    elem_filtro_categoria.addEventListener("change", filtrado);

    function filtrado() {
        let articulos = document.querySelectorAll("#galeria_general li");
        let valor_categoria_filtro = `Categoría: ${elem_filtro_categoria.value}`;

        articulos.forEach(articulo => {
            let valor_categoria_elemento = articulo.querySelector("p.categoria-art").textContent;

            if (valor_categoria_elemento === valor_categoria_filtro || valor_categoria_filtro === "Categoría: Todos los rubros") {
                articulo.style.display = "block"; //si coincide no lo borra de pantalla
            } else {
                articulo.style.display = "none"; //si no coincide, lo elimina de pantalla
            }
        });
    }
});
