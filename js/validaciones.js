/*Funciones de validación*/
function soloNumeros(texto) {
    for (let caracter of texto) {
        if (caracter < "0" || caracter > "9") {
            return false;
        }
    }
    return true;
}

function validarNombre(nombre) {
    let letras = 0;
    for (let caracter of nombre) {
        if (caracter >= "0" && caracter <= "9") {
            return false;
        }
        if (caracter !== " ") {
            letras++;
        }
    }
    return letras >= 2;
}

function validarDni(dni) {
    return dni.length === 8 && soloNumeros(dni);
}

function validarTelefono(telefono) {
    return telefono.length >= 10 && telefono.length <= 13 && soloNumeros(telefono);
}

function mostrarError(id, mensaje) {
    document.getElementById(id + "Error").innerHTML = mensaje;
}

/*Formulario de solicitud de artesano*/
document.addEventListener("DOMContentLoaded", function () {
    const formulario = document.getElementById("formArtesano");
    if (formulario !== null) {
        formulario.addEventListener("submit", validarFormularioArtesano);
    }
});

function validarFormularioArtesano(event) {
    event.preventDefault();
    let valido = true;

    const nombre = document.getElementById("nombre").value;
    const apellido = document.getElementById("apellido").value;
    const dni = document.getElementById("documento").value;
    const telefono = document.getElementById("telefono").value;

    mostrarError("nombre", "");
    mostrarError("apellido", "");
    mostrarError("documento", "");
    mostrarError("telefono", "");

    if (!validarNombre(nombre)) {
        mostrarError("nombre", "El nombre debe tener al menos 2 letras y no puede contener números");
        valido = false;
    }
    if (!validarNombre(apellido)) {
        mostrarError("apellido", "El apellido debe tener al menos 2 letras y no puede contener números");
        valido = false;
    }
    if (!validarDni(dni)) {
        mostrarError("documento", "El DNI debe contener 8 dígitos");
        valido = false;
    }
    if (!validarTelefono(telefono)) {
        mostrarError("telefono", "El teléfono debe tener entre 10 y 13 números, sin espacios ni guiones");
        valido = false;
    }

    if (valido) {
        alert("Solicitud enviada correctamente");
        document.getElementById("formArtesano").submit();
    }
}

/* Formulario de producto */
document.addEventListener("DOMContentLoaded", function () {
    const formulario = document.getElementById("formProducto");
    if (formulario !== null) {
        formulario.addEventListener("submit", validarFormularioProducto);
    }
});

function validarFormularioProducto(event) {
    //
}
