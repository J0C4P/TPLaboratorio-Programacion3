from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from ponchoVirtual.apps.artesanos.models import Artesano
from ponchoVirtual.apps.productos.forms import ProductoModificarForm, ProductoForm
from ponchoVirtual.apps.productos.models import Producto


def listar_productos(request):
    productos = Producto.objects.all()
    categorias = Producto.objects.values_list('categoria', flat=True).distinct()
    localidades = Producto.objects.values_list('localidad', flat=True).distinct()

    context = {'productos': productos, 'categorias': categorias, 'localidades': localidades}

    return render(request, 'Catalogo_general.html', context)


def mis_productos(request, artesano_dni):
    productos_artesano = Producto.objects.filter(artesano__dni=artesano_dni)

    return render(request, 'Mis_productos.html', {'productos_artesano': productos_artesano})


def detalles_producto(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)

    return render(request, 'detalle_producto.html', {'producto': producto})


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


def eliminar_producto(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)
    nombre = producto.nombre
    artesano = producto.artesano.dni

    producto.delete()
    messages.success(request, f'El producto {nombre} ha sido eliminado con exito!')

    return redirect('productos:mis_productos', artesano_dni=artesano)
