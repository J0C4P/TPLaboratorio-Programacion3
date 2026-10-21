from django.contrib import messages
from django.db.models import Model
from django.shortcuts import render, redirect, get_object_or_404
from ponchoVirtual.apps.artesanos.models import Artesano
from ponchoVirtual.apps.productos.forms import ProductoForm
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


def agregar_productos(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)

        if form.is_valid():
            producto = form.save(commit=False)

            # completado datos producto con artesano
            artesano_bd = get_object_or_404(Artesano, dni=request.user.documento_identidad)
            producto.artesano = artesano_bd
            producto.localidad = artesano_bd.localidad

            producto.save()

            messages.success(request, "¡El producto ha sido ingresado con exito!")
            return redirect('productos:mis_productos', request.user.documento_identidad)

    else:
        form = ProductoForm()

    return render(request, 'Crear_producto.html', {'form': form})
