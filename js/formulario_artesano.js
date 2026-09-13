/*Formulario de solicitud de artesano*/
function actualizarContador(id) {
    const campo = document.getElementById(id);
    document.getElementById(id + "Contador").innerHTML = campo.value.length + "/500";
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("descripcion").addEventListener("keyup", function () {
        actualizarContador("descripcion");
    });

    document.getElementById("experiencia").addEventListener("keyup", function () {
        actualizarContador("experiencia");
    });

    document.getElementById("botonLimpiar").addEventListener("click", function (event) {
        if (confirm("¿Querés borrar todos los datos del formulario?")) {
            mostrarError("nombre", "");
            mostrarError("apellido", "");
            mostrarError("documento", "");
            mostrarError("telefono", "");
            document.getElementById("descripcionContador").innerHTML = "0/500";
            document.getElementById("experienciaContador").innerHTML = "0/500";
        } else {
            event.preventDefault();
        }
    });
});
