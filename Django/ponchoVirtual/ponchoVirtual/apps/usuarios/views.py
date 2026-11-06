
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from ponchoVirtual.apps.artesanos.models import Stand
from django.db.models import Q
from django.shortcuts import render
from ponchoVirtual.apps.artesanos.models import Stand






from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from ponchoVirtual.apps.artesanos.forms import ArtesanoForm, EmprendimientoForm
from ponchoVirtual.apps.artesanos.models import Artesano, Stand
from ponchoVirtual.apps.usuarios.models import Usuario
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy


def login_vista(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            # para continuar el link en el que clickeo y no vuelva a principal
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)

            return redirect('principal')
        else:
            return render(request, 'login.html', {"msj": "Credenciales incorrectas"})
    # GET
    else:
        return render(request, 'login.html')


def logout_vista(request):
    logout(request)
    return redirect('principal')


def portada(request):
    # Coordenadas exactas centradas en los galpones del Predio Ferial
    pabellones_dict = {
        "Pabellón A: Textiles": {"lat": -28.4480, "lng": -65.7583, "stands": []},
        "Pabellón B: Cerámica": {"lat": -28.4482, "lng": -65.7570, "stands": []},
        "Pabellón C: Gastronomía regional": {"lat": -28.4495, "lng": -65.7573, "stands": []},
        "Pabellón D: Orfebreria y Joyeria": {"lat": -28.4475, "lng": -65.7576, "stands": []},
    }

    # Traemos todos los stands con su artesano y emprendimiento en vivo
    stands_db = Stand.objects.select_related('artesano__emprendimiento').order_by('numero')

    for st in stands_db:
        zona_texto = (st.zona or "").upper()
        
        # Mapeamos según la letra del pabellón
        if "B" in zona_texto:
            destino = "Pabellón B: Cerámica"
        elif "C" in zona_texto:
            destino = "Pabellón C: Gastronomía regional"
        elif "D" in zona_texto:
            destino = "Pabellón D: Orfebreria y Joyeria"
        else:
            destino = "Pabellón A: Textiles"

        tiene_artesano = st.artesano is not None
        artesano_nom = f"{st.artesano.nombre_artesano} {st.artesano.apellido}" if tiene_artesano else None
        
        emp_nom = None
        emp_rubro = None
        if tiene_artesano:
            try:
                emp = st.artesano.emprendimiento
                if emp:
                    emp_nom = emp.nombre_emprendimiento
                    emp_rubro = emp.rubro
            except Exception:
                emp_nom = None

        pabellones_dict[destino]["stands"].append({
            "numero": st.numero,
            "ocupado": tiene_artesano,
            "artesano": artesano_nom,
            "emprendimiento": emp_nom,
            "rubro": emp_rubro
        })

    # Pasamos el diccionario directo (Django se encarga de serializarlo en el template)
    contexto = {
        "datos_mapa": pabellones_dict,
    }
    return render(request, "base/portada.html", contexto)


@login_required(login_url=reverse_lazy('usuario:login'))
def cambiar_contraseña(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Importante para que no se cierre la sesión
            messages.success(request, '¡Contraseña actualizada con éxito!')
            return redirect('usuario:cambiar_contraseña')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'cambiar_contraseña.html', {'form': form})


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

            # 1. Guardamos el motivo en su campo independiente
            artesano.motivo_rechazo = motivo
            artesano.save()

            # 2. Desactivamos al usuario y liberamos stand (sin tocar observaciones)
            usuario.is_active = False
            usuario.save()
            Stand.objects.filter(artesano=artesano).update(artesano=None)

            messages.warning(request, f"La solicitud con DNI {dni} ha sido rechazada.")
            return redirect('usuario:solicitudes_rechazadas_admin')

    return render(request, 'mas_detalles_solicitud.html', {
        'usuario': usuario,
        'artesano': artesano,
        'stands_disponibles': stands_disponibles
    })


def modificar_solicitud(request, dni):
    artesano = get_object_or_404(Artesano, dni=dni)
    emprendimiento = artesano.emprendimiento
    if request.method == "POST":
        form_artesano = ArtesanoForm(request.POST, instance=artesano)
        form_emprendimiento = EmprendimientoForm(request.POST, instance=emprendimiento)

        if form_artesano.is_valid() and form_emprendimiento.is_valid():

            emprendimiento = form_emprendimiento.save()
            artesano = form_artesano.save(commit=False)
            artesano.emprendimiento = emprendimiento
            artesano.save()
            return redirect('usuario:consultar_estado_solicitud')

    else:
        form_artesano = ArtesanoForm(instance=artesano)
        form_emprendimiento = EmprendimientoForm(instance=emprendimiento)

    return render(request, 'modificar_solicitud.html', {'form_artesano': form_artesano, 'form_emprendimiento': form_emprendimiento})


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
def solicitudes_artesanos_admin(request):
    if not request.user.is_staff:
        raise PermissionDenied

    usuarios_inactivos = Usuario.objects.filter(is_active=False)
    dnis_usuarios_inactivos = usuarios_inactivos.values_list('documento_identidad', flat=True)

    # Solo postulantes inactivos que NO tengan motivo de rechazo (o que sea vacío)
    artesanos = Artesano.objects.filter(
        dni__in=dnis_usuarios_inactivos
    ).filter(
        Q(motivo_rechazo__isnull=True) | Q(motivo_rechazo="")
    ).select_related('emprendimiento').order_by('-id')

    return render(request, 'solicitudes_artesanos.html', {'artesanos': artesanos})


@login_required(login_url=reverse_lazy('usuario:login'))
def solicitudes_rechazadas_admin(request):
    if not request.user.is_staff:
        raise PermissionDenied

    # Trae a todos los artesanos que SÍ tienen un motivo de rechazo cargado
    artesanos_rechazados = Artesano.objects.filter(
        motivo_rechazo__isnull=False
    ).exclude(
        motivo_rechazo=""
    ).select_related('emprendimiento').order_by('-id')

    return render(request, 'solicitudes_rechazadas.html', {
        'artesanos_rechazados': artesanos_rechazados
    })


def consultar_estado_solicitud(request):
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

