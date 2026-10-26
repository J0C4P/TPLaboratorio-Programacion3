from django.contrib import admin
from ponchoVirtual.apps.productos.models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'descripcion', 'precio', 'localidad', 'imagen', 'stock', 'fecha_publicacion', 'artesano', 'activo']
    search_fields = ('nombre', 'categoria')
    list_filter = ('categoria', 'localidad', 'activo')
