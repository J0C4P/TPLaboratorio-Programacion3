from django.db.models import Model
from django.shortcuts import render
from ponchoVirtual.apps.productos.models import Producto


def listar_productos(request):
    productos = Producto.objects.all()

    return render(request, 'Catalogo_general.html', {'productos': productos})


def mis_productos(request, artesano_dni):
    productos_artesano = Producto.objects.filter(artesano__dni=artesano_dni)

    return render(request, 'Mis_productos.html', {'productos_artesano': productos_artesano})

