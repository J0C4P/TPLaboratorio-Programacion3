from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from ponchoVirtual.apps.artesanos.forms import ArtesanoForm, EmprendimientoForm, Artesano, ArtesanoModificarForm, EmprendimientoModificarForm
from ponchoVirtual.apps.artesanos.models import Stand
from ponchoVirtual.utils.pdf import generar_reporte_pdf


def solicitud_artesano(request):
    if request.method == "POST":
        form_artesano = ArtesanoForm(request.POST)
        form_emprendimiento = EmprendimientoForm(request.POST)

        if form_artesano.is_valid() and form_emprendimiento.is_valid():
            emprendimiento = form_emprendimiento.save()
            artesano = form_artesano.save(commit=False)

            artesano.emprendimiento = emprendimiento

            artesano.save()
            messages.success(request, "¡Registro completado con éxito!")
            return redirect('productos:listar_productos')
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


@login_required(login_url=reverse_lazy('usuario:login'))
def reporte_artesanos_pdf(request):
    if not request.user.is_staff:
        raise PermissionDenied

    artesanos = Artesano.objects.select_related('emprendimiento').order_by('apellido', 'nombre')

    filas = [
        (f'{a.apellido}, {a.nombre}', a.dni, a.emprendimiento.nombre, f'{a.localidad} ({a.provincia})',
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
    for a in Artesano.objects.order_by('apellido', 'nombre'):
        nombres.setdefault((a.localidad, a.provincia), []).append(f'{a.apellido}, {a.nombre}')

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
         f'{s.artesano.apellido}, {s.artesano.nombre}' if s.artesano else '-')
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
