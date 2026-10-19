let articulos_favoritos = [];

document.addEventListener("DOMContentLoaded", () => {
    const estrellas = document.querySelectorAll(".boton_fav");

    estrellas.forEach((estrella) => {
        estrella.addEventListener("click", function() {
            if(estrella.textContent === "☆"){
                estrella.textContent = "★";
                estrella.style.color = "gold";
            }
            else{
                estrella.textContent = "☆";
                estrella.style.color = "gray";
            }
        })
    })
});

document.addEventListener("DOMContentLoaded", () =>{
    const estrellas = document.querySelectorAll(".boton_fav");
    const barra_fav = document.querySelector("ul#menu_favoritos");

    estrellas.forEach(estrella => {
        estrella.addEventListener("click", (event) =>{
            let card_favorito = event.target.parentElement.parentElement;
            let titulo = card_favorito.querySelector("h3.card-title").textContent;

            if(estrella.style.color === "gold") {
                articulos_favoritos.push(card_favorito);
                const elemento_fav = document.createElement("li");
                const elemento_titulo_fav = document.createElement("p");
                elemento_titulo_fav.innerHTML = `<p class="dropdown-item-text" id="${card_favorito.id}">${titulo}</p>`;

                elemento_fav.appendChild(elemento_titulo_fav);
                barra_fav.appendChild(elemento_fav);
            }
            else if(estrella.style.color === "gray"){
                //articulos_favoritos.;
                let elemento_eliminar_fav = barra_fav.querySelector(`li p[id="${card_favorito.id}"]`);
                elemento_eliminar_fav.parentNode.removeChild(elemento_eliminar_fav);
                
            }

        })
    })
});