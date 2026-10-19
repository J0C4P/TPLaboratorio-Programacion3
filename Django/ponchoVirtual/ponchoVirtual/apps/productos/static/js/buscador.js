document.addEventListener("DOMContentLoaded", () =>{
    let btn_buscador = document.getElementById("buscador_texto").querySelector("button[type='submit']")
    let input_buscador = document.getElementById("buscador_texto").querySelector("input[type='search']");

    btn_buscador.addEventListener("click", () => {
        let texto_a_buscar = input_buscador.value.toLowerCase();
        let articulos = document.getElementById("galeria_general").querySelectorAll("li");

        articulos.forEach(articulo =>{
            let titulo = articulo.querySelector("div.card-body h3").textContent.toLowerCase();
            let elementos_textuales = articulo.querySelectorAll("div.card-body p");

            let i;
            for(i = 0; i < elementos_textuales.length; i++){
                let texto = elementos_textuales[i].textContent.toLowerCase();

                if(titulo.includes(texto_a_buscar) || texto.includes(texto_a_buscar)){
                    articulo.style.display = "block";
                    break;
                }
                else{
                    articulo.style.display = "none";
                }
            }
        })
    })
});