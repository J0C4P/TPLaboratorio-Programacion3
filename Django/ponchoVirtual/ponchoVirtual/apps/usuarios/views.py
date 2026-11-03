from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from ponchoVirtual.apps.artesanos.models import Artesano, Stand
from ponchoVirtual.apps.usuarios.models import Usuario
from django.contrib import messages


def login_vista(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('principal')
        else:
            return render(request, 'login.html', {"msj": "Credenciales incorrectas"})
    # GET
    else:
        return render(request, 'login.html')


def logout_vista(request):
    logout(request)
    return redirect('principal')


@login_required(login_url=reverse_lazy('usuario:login'))
def solicitudes_artesanos_admin(request):
    if not request.user.is_staff:
        raise PermissionDenied

    # 1. Buscamos los DNI de usuarios inactivos
    usuarios_inactivos = Usuario.objects.filter(is_active=False)
    dnis_usuarios_inactivos = usuarios_inactivos.values_list('documento_identidad', flat=True)

    # 2. Excluimos los que contengan la marca "RECHAZADO:" en sus observaciones
    artesanos = Artesano.objects.filter(
        dni__in=dnis_usuarios_inactivos
    ).exclude(
        emprendimiento__observaciones__icontains="RECHAZADO:"
    )

    return render(request, 'solicitudes_artesanos.html', {'artesanos': artesanos})


@login_required(login_url=reverse_lazy('usuario:login'))
def evaluar_solicitud_admin(request, dni):
    if not request.user.is_staff:
        raise PermissionDenied

    artesano = get_object_or_404(Artesano, dni=dni)
    usuario = get_object_or_404(Usuario, documento_identidad=dni)
    stands_disponibles = Stand.objects.filter(artesano__isnull=True)

    if request.method == "POST":
        accion = request.POST.get('accion')

        if accion == 'aprobar':
            stand_id = request.POST.get('stand_id')
            if not stand_id:
                messages.error(request, "Debe seleccionar un Stand / Pabellón para aprobar al artesano.")
                return render(request, 'mas_detalles_solicitud.html', {
                    'usuario': usuario,
                    'artesano': artesano,
                    'stands_disponibles': stands_disponibles
                })

            stand_seleccionado = get_object_or_404(Stand, id=stand_id)
            stand_seleccionado.artesano = artesano
            stand_seleccionado.save()

            usuario.is_active = True
            usuario.save()

            # Le asignamos el rol correspondiente a artesano
            grupo_permisos = Group.objects.get(name='rol_artesano')
            usuario.groups.add(grupo_permisos)

            messages.success(request, f"Solicitud aprobada con éxito. Stand {stand_seleccionado.numero} asignado.")
            return redirect('usuario:solicitudes_artesanos_admin')

        elif accion == 'rechazar':
            motivo = request.POST.get('motivo_rechazo', '').strip()
            if not motivo:
                messages.error(request, "Debe ingresar el motivo del rechazo para informar al postulante.")
                return render(request, 'mas_detalles_solicitud.html', {
                    'usuario': usuario,
                    'artesano': artesano,
                    'stands_disponibles': stands_disponibles
                })


            # Guardamos el motivo en las observaciones del emprendimiento
            emprendimiento = artesano.emprendimiento
            emprendimiento.observaciones = f"RECHAZADO: {motivo}"
            emprendimiento.save()

            # Mantenemos al usuario inactivo (sin borrarlo)
            usuario.is_active = False
            usuario.save()

            messages.warning(request, f"La solicitud del DNI {dni} ha sido rechazada.")

            messages.warning(request, f"La solicitud con DNI {dni} ha sido rechazada.")

            return redirect('usuario:solicitudes_artesanos_admin')

    return render(request, 'mas_detalles_solicitud.html', {
        'usuario': usuario,
        'artesano': artesano,
        'stands_disponibles': stands_disponibles
    })


@login_required(login_url=reverse_lazy('usuario:login'))
def reconsiderar_solicitud_admin(request, dni):
    if not request.user.is_staff:
        raise PermissionDenied

    artesano = get_object_or_404(Artesano, dni=dni)

    # Limpiamos el motivo de rechazo del emprendimiento
    if artesano.emprendimiento:
        artesano.emprendimiento.observaciones = ""
        artesano.emprendimiento.save()

    messages.info(request,
                  f"La postulación de {artesano.nombre_artesano} {artesano.apellido} volvió a estado pendiente para su evaluación.")

    # Redirige directamente a la pantalla de evaluar
    return redirect('usuario:evaluar_solicitud_admin', dni=artesano.dni)


@login_required(login_url=reverse_lazy('usuario:login'))
def solicitudes_rechazadas_admin(request):
    if not request.user.is_staff:
        raise PermissionDenied

    # Traemos los artesanos que tienen la marca de rechazo en observaciones
    artesanos_rechazados = Artesano.objects.filter(
        emprendimiento__observaciones__startswith="RECHAZADO:"
    ).select_related('emprendimiento').order_by('-id')

    return render(request, 'solicitudes_rechazadas.html', {
        'artesanos_rechazados': artesanos_rechazados
    })


def consultar_estado_solicitud(request):
    usuario = None
    artesano = None

    if request.method == "POST":
        dni_ingresado = request.POST.get('dni', '').strip()
        usuario = Usuario.objects.filter(documento_identidad=dni_ingresado).first()
        if usuario:
            artesano = Artesano.objects.filter(dni=dni_ingresado).select_related('emprendimiento', 'stand').first()

        return render(request, 'estado_solicitud.html', {'usuario': usuario, 'artesano': artesano})

    return render(request, 'estado_solicitud.html')


@login_required(login_url=reverse_lazy('usuario:login'))
def listar_artesanos_aceptados(request):
    if not request.user.is_staff:
        raise PermissionDenied

    dnis_activos = Usuario.objects.filter(is_active=True, is_staff=False).values_list('documento_identidad', flat=True)
    artesanos = Artesano.objects.filter(dni__in=dnis_activos).select_related('emprendimiento', 'stand')
    stands_disponibles = Stand.objects.filter(artesano__isnull=True)

    if request.method == "POST":
        accion = request.POST.get('accion')
        artesano_id = request.POST.get('artesano_id')
        artesano = get_object_or_404(Artesano, id=artesano_id)

        # CASO A: Quitar rol / Dar de baja
        if accion == 'dar_de_baja':
            # 1. Liberar el stand que ocupaba y eliminar todos sus datos y emprendimiento
            Stand.objects.filter(artesano=artesano).update(artesano=None)
            artesano.emprendimiento.delete() # Eliminamos el emprendimiento y por cascada se elimina el artesano

            # 2. Desactivar el usuario y quitarle permisos/grupos
            usuario = Usuario.objects.filter(documento_identidad=artesano.dni).first()
            if usuario:
                usuario.groups.clear()     # Se le quita el grupo 'Artesano'
                usuario.user_permissions.clear()  # Se le limpian permisos individuales
                usuario.delete()

            messages.warning(request, f"Se dieron de baja los permisos y el stand del artesano {artesano.nombre_artesano} {artesano.apellido}.")
            return redirect('usuario:listar_artesanos_aceptados')

        # CASO B: Reasignar stand
        nuevo_stand_id = request.POST.get('nuevo_stand_id')
        if nuevo_stand_id:
            Stand.objects.filter(artesano=artesano).update(artesano=None)
            nuevo_stand = get_object_or_404(Stand, id=nuevo_stand_id)
            nuevo_stand.artesano = artesano
            nuevo_stand.save()
            messages.success(request, f"Se actualizó la ubicación de {artesano.nombre_artesano}.")

        return redirect('usuario:listar_artesanos_aceptados')

    return render(request, 'artesanos_aceptados.html', {
        'artesanos': artesanos,
        'stands_disponibles': stands_disponibles
    })

