from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from ponchoVirtual.apps.artesanos.forms import ArtesanoForm, EmprendimientoForm, Artesano, ArtesanoModificarForm, EmprendimientoModificarForm
# Importamos el modelo Usuario y el Group de permisos
from ponchoVirtual.apps.usuarios.models import Usuario
from django.contrib.auth.models import Group

def solicitud_artesano(request):
    if request.method == "POST":
        print(">>> LLEGÓ LA PETICIÓN POST AL SERVIDOR")
        form_artesano = ArtesanoForm(request.POST)
        form_emprendimiento = EmprendimientoForm(request.POST)


        #esto valida que los datos no tengan errores
        if form_artesano.is_valid() and form_emprendimiento.is_valid():
            dni = str(form_artesano.cleaned_data['dni'])
            email = form_artesano.cleaned_data['correo']
            nombre = form_artesano.cleaned_data['nombre']
            apellido = form_artesano.cleaned_data['apellido']

            #  Valida que no existe  un usuario con ese dni
            if Usuario.objects.filter(username=dni).exists() or Usuario.objects.filter(documento_identidad=dni).exists():
                messages.error(request, "Ya existe una solicitud o usuario registrado con este DNI.")
                return render(request, 'Crear_art_emp.html', {'form_art': form_artesano, 'form_emp': form_emprendimiento})

            # si no exite lo guarda con los parametros del datos del emprendimiento y la persona 
            emprendimiento = form_emprendimiento.save()
            artesano = form_artesano.save(commit=False)
            artesano.emprendimiento = emprendimiento
            artesano.save()

            # Crear el usuario pendiente
            Usuario.objects.create_user(
                username=dni,
                email=email,
                password=dni,
                first_name=nombre,
                last_name=apellido,
                documento_identidad=dni,
                is_active=False  # Inactivo hasta que el administrador lo apruebe en el Admin
            )

            # Renderizar pantalla  con boton de volver al inicio
           #  Mostrar la pantalla   estado pendiente
            contexto = {
                'nombre': nombre,
                'apellido': apellido,
                'dni': dni
            }
            return render(request, 'solicitud_pendiente.html', contexto)

           
    else:
        form_artesano = ArtesanoForm()
        form_emprendimiento = EmprendimientoForm()

    return render(request, 'Crear_art_emp.html', {'form_art': form_artesano, 'form_emp': form_emprendimiento})



def datos_artesano(request, dni_artesano):
    artesano = get_object_or_404(Artesano, dni=dni_artesano)
    emprendimiento = artesano.emprendimiento

    return render(request, 'artesano.html', {'artesano': artesano, 'emprendimiento': emprendimiento})


def modificar_datos_art(request, dni_artesano):
    artesano = get_object_or_404(Artesano, dni=dni_artesano)
    emprendimiento = artesano.emprendimiento

    if request.method == "POST":
        form_art = ArtesanoModificarForm(request.POST, instance=artesano)
        form_emp = EmprendimientoModificarForm(request.POST, instance=emprendimiento)
        if form_art.is_valid() and form_emp.is_valid():
            emprendimiento = form_emp.save()
            artesano = form_art.save(commit=False)

            artesano.emprendimiento = emprendimiento

            artesano.save()
            messages.success(request, f'El perfil del artesano {artesano.nombre} {artesano.apellido} ha sido modificado exitosamente!')
            return redirect('artesano:datos_artesano', dni_artesano=artesano.dni)

    else:
        form_art = ArtesanoModificarForm(instance=artesano)
        form_emp = EmprendimientoModificarForm(instance=emprendimiento)
    return render(request, 'Crear_art_emp.html', {'form_art': form_art, 'form_emp': form_emp})