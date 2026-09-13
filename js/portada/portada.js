
document.addEventListener("DOMContentLoaded", function () {
    
    const input_comentarios = document.getElementById("Comentario");
    const enviar = document.getElementById("enviar");

    if (enviar) {
        enviar.addEventListener("click", function (event) {
            
            // defino  una variable obteniendo el valor del textarea que seria guardar
            //el texto del usuaro en un variable local 
            const textoComentario = input_comentarios.value.trim();
            
            // Validacion de longitud
            if (textoComentario.length <2) {
                alert("El comentario es muy corto. Por favor, ingresá al menos 3 caracteres.");
                
                return;
            }

           

            alert("¡Muchas gracias por tu comentario y sugerencia!");
            
            input_comentarios.value = "";
        });
    }
});