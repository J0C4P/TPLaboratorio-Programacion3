from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from ponchoVirtual.apps.artesanos.models import Artesano
from ponchoVirtual.apps.productos.forms import ProductoModificarForm, ProductoForm
from ponchoVirtual.apps.productos.models import Producto
from ponchoVirtual.utils.pdf import generar_reporte_pdf


def listar_productos(request):
    productos = Producto.objects.all()
    categorias = Producto.objects.values_list('categoria', flat=True).distinct()
    localidades = Producto.objects.values_list('localidad', flat=True).distinct()

    context = {'productos': productos, 'categorias': categorias, 'localidades': localidades}

    return render(request, 'Catalogo_general.html', context)


def ver_productos_artesano(request, artesano_dni):
    productos_artesano = Producto.objects.filter(artesano__dni=artesano_dni)
    artesano = get_object_or_404(Artesano, dni=artesano_dni)

    return render(request, 'Productos_artesano.html',{'productos_artesano': productos_artesano, 'artesano': artesano})


@login_required(login_url='usuario:login')
def ver_mis_productos(request, artesano_dni):
    productos_artesano = Producto.objects.filter(artesano__dni=artesano_dni)

    return render(request, 'Mis_productos.html',{'productos_artesano': productos_artesano, 'artesano_dni': artesano_dni})


@login_required(login_url=reverse_lazy('usuario:login'))
def reporte_productos_artesano_pdf(request, artesano_dni):
    if not (request.user.is_staff or request.user.documento_identidad == artesano_dni):
        raise PermissionDenied

    artesano = get_object_or_404(Artesano, dni=artesano_dni)
    productos = Producto.objects.filter(artesano=artesano).order_by('categoria', 'nombre')

    filas = [
        (p.nombre, p.categoria, f'$ {p.precio:.2f}', p.stock, 'Activo' if p.activo else 'Inactivo',
         timezone.localtime(p.fecha_publicacion).strftime('%d/%m/%Y'))
        for p in productos
    ]
    valor_stock = sum(p.precio * p.stock for p in productos)

    return generar_reporte_pdf(
        nombre_archivo=f'productos_{artesano.dni}.pdf',
        titulo='Productos publicados por artesano',
        subtitulo=f'Artesano: {artesano.nombre} {artesano.apellido} (DNI {artesano.dni}) - '
                  f'Emprendimiento: {artesano.emprendimiento.nombre}',
        encabezados=('Producto', 'Categoría', 'Precio', 'Stock', 'Estado', 'Publicado'),
        filas=filas,
        anchos=(4, 2.5, 2, 1.2, 1.8, 2),
        totales=[('Productos publicados', len(filas)), ('Valor total del stock', f'$ {valor_stock:.2f}')],
    )


@login_required(login_url='usuario:login')
def detalles_producto(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)

    return render(request, 'detalle_producto.html', {'producto': producto})


@login_required(login_url='usuario:login')
def agregar_productos(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)

        if form.is_valid():
            producto = form.save(commit=False)
            nombre = producto.nombre
            # completado datos producto con artesano
            artesano_bd = get_object_or_404(Artesano, dni=request.user.documento_identidad)
            producto.artesano = artesano_bd
            producto.localidad = artesano_bd.localidad

            producto.save()

            messages.success(request, f'¡El producto "{nombre}" ha sido ingresado con exito!')
            return redirect('productos:mis_productos', request.user.documento_identidad)

    else:
        form = ProductoForm()

    return render(request, 'Crear_producto.html', {'form': form})


@login_required(login_url='usuario:login')
def modificar_producto(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)
    if request.method == 'POST':
        form_prod = ProductoModificarForm(request.POST, request.FILES, instance=producto)

        if form_prod.is_valid():
            form_prod.save()
            messages.success(request, f'Se ha actualizado correctamente el Anuncio "{producto.nombre}"')
            return redirect('productos:detalles_producto', id_producto=producto.id)
    else:
        form_prod = ProductoModificarForm(instance=producto)
    return render(request, 'Crear_producto.html', {'form': form_prod})


@login_required(login_url='usuario:login')
def eliminar_producto(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)
    nombre = producto.nombre
    artesano = producto.artesano.dni

    producto.delete()
    messages.success(request, f'El producto {nombre} ha sido eliminado con exito!')

    return redirect('productos:mis_productos', artesano_dni=artesano)


@login_required(login_url=reverse_lazy('usuario:login'))
def reporte_artesanos_rubro_pdf(request):
    if not request.user.is_staff:
        raise PermissionDenied

    productos = Producto.objects.filter(activo=True).select_related('artesano')

    por_rubro = {}
    for p in productos:
        rubro = por_rubro.setdefault(p.categoria, {'artesanos': set(), 'productos': 0})
        rubro['artesanos'].add(f'{p.artesano.apellido}, {p.artesano.nombre}')
        rubro['productos'] += 1

    filas = [
        (categoria, len(datos['artesanos']), datos['productos'], '; '.join(sorted(datos['artesanos'])))
        for categoria, datos in sorted(por_rubro.items(), key=lambda item: (-len(item[1]['artesanos']), item[0]))
    ]

    sin_productos = Artesano.objects.exclude(productos_artesano__activo=True).order_by('apellido', 'nombre')
    if sin_productos:
        filas.append(('Sin productos publicados', len(sin_productos), 0,
                      '; '.join(f'{a.apellido}, {a.nombre}' for a in sin_productos)))

    return generar_reporte_pdf(
        nombre_archivo='artesanos_por_rubro.pdf',
        titulo='Artesanos registrados por rubro',
        subtitulo='El rubro es la categoría de los productos activos; un artesano figura en cada rubro en el que publica',
        encabezados=('Rubro', 'Artesanos', 'Productos', 'Detalle de artesanos'),
        filas=filas,
        anchos=(3.2, 1.7, 1.7, 7),
        totales=[('Total de artesanos registrados', Artesano.objects.count())],
    )
