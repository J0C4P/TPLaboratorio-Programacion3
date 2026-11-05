from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from ponchoVirtual.apps.artesanos.forms import ArtesanoForm, EmprendimientoForm, Artesano, ArtesanoModificarForm, EmprendimientoModificarForm, StandForm
from ponchoVirtual.apps.artesanos.models import Stand, Artesano
from ponchoVirtual.utils.pdf import generar_reporte_pdf
from ponchoVirtual.apps.usuarios.models import Usuario
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404

from ponchoVirtual.apps.artesanos.models import Artesano


def solicitud_artesano(request):
    if request.method == "POST":
        form_artesano = ArtesanoForm(request.POST)
        form_emprendimiento = EmprendimientoForm(request.POST)

        # esto valida que los datos no tengan errores
        if form_artesano.is_valid() and form_emprendimiento.is_valid():
            dni = str(form_artesano.cleaned_data['dni'])
            email = form_artesano.cleaned_data['correo']
            nombre = form_artesano.cleaned_data['nombre_artesano']
            apellido = form_artesano.cleaned_data['apellido']

            #  Valida que no existe  un usuario con ese dni
            if Usuario.objects.filter(username=dni).exists() or Usuario.objects.filter(
                    documento_identidad=dni).exists():
                messages.error(request, "Ya existe una solicitud o usuario registrado con este DNI.")
                return render(request, 'Crear_art_emp.html',
                              {'form_art': form_artesano, 'form_emp': form_emprendimiento})

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


@login_required(login_url='usuario:login')
@permission_required('artesanos.change_artesano', raise_exception=True)
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
            messages.success(request, f'El perfil del artesano {artesano.nombre_artesano} {artesano.apellido} ha sido modificado exitosamente!')
            return redirect('artesano:datos_artesano', dni_artesano=artesano.dni)

    else:
        form_art = ArtesanoModificarForm(instance=artesano)
        form_emp = EmprendimientoModificarForm(instance=emprendimiento)
    return render(request, 'Crear_art_emp.html', {'form_art': form_art, 'form_emp': form_emp})


@login_required(login_url=reverse_lazy('usuario:login'))
def reporte_artesanos_pdf(request):
    if not request.user.is_staff:
        raise PermissionDenied

    artesanos = Artesano.objects.select_related('emprendimiento').order_by('apellido', 'nombre_artesano')

    filas = [
        (f'{a.apellido}, {a.nombre_artesano}', a.dni, a.emprendimiento.nombre_emprendimiento, f'{a.localidad} ({a.provincia})',
         f'{a.correo} / {a.telefono}')
        for a in artesanos
    ]

    return generar_reporte_pdf(
        nombre_archivo='artesanos_registrados.pdf',
        titulo='Artesanos registrados',
        subtitulo='Listado de artesanos con su emprendimiento y datos de contacto',
        encabezados=('Artesano', 'DNI', 'Emprendimiento', 'Localidad', 'Contacto'),
        filas=filas,
        anchos=(3, 1.6, 3, 3, 4),
        totales=[('Total de artesanos', len(filas))],
    )


@login_required(login_url=reverse_lazy('usuario:login'))
def reporte_artesanos_localidad_pdf(request):
    if not request.user.is_staff:
        raise PermissionDenied

    localidades = (Artesano.objects.values('localidad', 'provincia')
                   .annotate(total=Count('id')).order_by('-total', 'localidad'))

    nombres = {}
    for a in Artesano.objects.order_by('apellido', 'nombre_artesano'):
        nombres.setdefault((a.localidad, a.provincia), []).append(f'{a.apellido}, {a.nombre_artesano}')

    filas = [
        (l['localidad'], l['provincia'], l['total'], '; '.join(nombres[(l['localidad'], l['provincia'])]))
        for l in localidades
    ]

    return generar_reporte_pdf(
        nombre_archivo='artesanos_por_localidad.pdf',
        titulo='Artesanos registrados por localidad',
        subtitulo='Cantidad de artesanos agrupados por localidad y provincia',
        encabezados=('Localidad', 'Provincia', 'Cantidad', 'Artesanos'),
        filas=filas,
        anchos=(3, 2.2, 1.6, 7),
        totales=[('Localidades', len(filas)), ('Total de artesanos', sum(l['total'] for l in localidades))],
    )


@login_required(login_url=reverse_lazy('usuario:login'))
def reporte_stands_pdf(request):
    if not request.user.is_staff:
        raise PermissionDenied

    stands = Stand.objects.select_related('artesano')

    filas = [
        (s.numero, s.zona, 'Ocupado' if s.artesano else 'Disponible',
         f'{s.artesano.apellido}, {s.artesano.nombre_artesano}' if s.artesano else '-')
        for s in stands
    ]
    ocupados = sum(1 for s in stands if s.artesano)

    return generar_reporte_pdf(
        nombre_archivo='stands_ocupados_disponibles.pdf',
        titulo='Stands ocupados y disponibles',
        subtitulo='Estado de ocupación de los stands del predio',
        encabezados=('Stand', 'Zona', 'Estado', 'Artesano asignado'),
        filas=filas,
        anchos=(1.5, 4, 2.5, 6),
        totales=[('Total de stands', len(filas)), ('Ocupados', ocupados), ('Disponibles', len(filas) - ocupados)],
    )


@login_required(login_url=reverse_lazy('usuario:login'))
def modificar_stand_artesano(request, artesano_id):
    if not request.user.is_staff:
        raise PermissionDenied

    artesano = get_object_or_404(Artesano, id=artesano_id)
    # Stand actual del artesano (si tiene uno asignado)
    stand_actual = getattr(artesano, 'stand', None)

    # Stands disponibles + el stand que actualmente ya posee
    stands_opciones = Stand.objects.filter(artesano__isnull=True)
    if stand_actual:
        stands_opciones = (stands_opciones | Stand.objects.filter(id=stand_actual.id)).distinct()

    if request.method == "POST":
        nuevo_stand_id = request.POST.get('stand_id')

        # Si el usuario selecciono un stand
        if nuevo_stand_id:
            nuevo_stand = get_object_or_404(Stand, id=nuevo_stand_id)

            # Si ya tenia un stand distinto asignado, lo liberamos
            if stand_actual and stand_actual.id != nuevo_stand.id:
                stand_actual.artesano = None
                stand_actual.save()

            # Asignamos el nuevo stand
            nuevo_stand.artesano = artesano
            nuevo_stand.save()

            messages.success(
                request,
                f"Ubicación actualizada: {artesano.nombre_artesano} ahora está en el Stand N° {nuevo_stand.numero} ({nuevo_stand.zona})."
            )
        else:
            # Opcion dejarlo sin stand
            if stand_actual:
                stand_actual.artesano = None
                stand_actual.save()
                messages.warning(request, f"Se ha retirado la asignación de stand a {artesano.nombre_artesano}.")

        return redirect('artesano:listar_artesanos_aceptados')

    return render(request, 'modificar_stand_artesano.html', {
        'artesano': artesano,
        'stand_actual': stand_actual,
        'stands_opciones': stands_opciones
    })




@login_required(login_url=reverse_lazy('usuario:login'))
def solicitudes_rechazadas_admin(request):
    if not request.user.is_staff:
        raise PermissionDenied

    # Filtramos por el estado propio del artesano o de su postulación
    artesanos_rechazados = Artesano.objects.filter(
        estado="RECHAZADO" 
    ).select_related('emprendimiento').order_by('-id')

@login_required(login_url='usuario:login')
@permission_required('artesanos.view_stand', raise_exception=True)
def gestion_stands(request):
    stands = Stand.objects.select_related('artesano').order_by('zona', 'numero')
    dnis_aprobados = Usuario.objects.filter(is_active=True).values('documento_identidad')
    artesanos_sin_stand = Artesano.objects.filter(stand__isnull=True, dni__in=dnis_aprobados)
    ocupados = sum(1 for s in stands if s.artesano_id)
    contexto = {
        'stands': stands,
        'artesanos_sin_stand': artesanos_sin_stand,
        'total': len(stands),
        'ocupados': ocupados,
        'disponibles': len(stands) - ocupados,
    }
    return render(request, 'gestion_stands.html', contexto)



@login_required(login_url='usuario:login')
@permission_required('artesanos.add_stand', raise_exception=True)
def crear_stand(request):
    if request.method == "POST":
        form = StandForm(request.POST)
        if form.is_valid():
            stand = form.save()
            messages.success(request, f'Se creó el {stand}.')
            return redirect('artesano:gestion_stands')
    else:
        form = StandForm()
    return render(request, 'crear_stand.html', {'form': form})



    artesano = get_object_or_404(Artesano, dni=dni)
    
    # Actualizamos el estado del artesano a PENDIENTE
    artesano.estado = "PENDIENTE"
    artesano.save()

    # NOTA: Ya no tocamos artesano.emprendimiento.observaciones
    # para no borrar los datos reales del taller.

    messages.info(request, f"La postulación de {artesano.nombre_artesano} {artesano.apellido} volvió a estado pendiente para su evaluación.")
    
    return redirect('artesano:evaluar_solicitud_admin', dni=artesano.dni)

@login_required(login_url='usuario:login')
@permission_required('artesanos.change_stand', raise_exception=True)
@require_POST
def asignar_stand(request, id_stand):
    stand = get_object_or_404(Stand, id=id_stand)
    artesano = get_object_or_404(Artesano, id=request.POST.get('artesano'))

    if stand.artesano_id:
        messages.error(request, f'El {stand} ya está ocupado. Libéralo antes de asignarlo.')
    elif Stand.objects.filter(artesano=artesano).exists():
        messages.error(request, f'{artesano} ya tiene un stand asignado.')
    else:
        stand.artesano = artesano
        stand.save()
        messages.success(request, f'{artesano} fue asignado al {stand}.')
    return redirect('artesano:gestion_stands')


@login_required(login_url='usuario:login')
@permission_required('artesanos.change_stand', raise_exception=True)
@require_POST
def liberar_stand(request, id_stand):
    stand = get_object_or_404(Stand, id=id_stand)
    if stand.artesano_id:
        stand.artesano = None
        stand.save()
        messages.success(request, f'El {stand} fue liberado.')
    else:
        messages.info(request, f'El {stand} ya estaba disponible.')
    return redirect('artesano:gestion_stands')

