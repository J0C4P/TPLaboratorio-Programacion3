from django.contrib import admin
from ponchoVirtual.apps.artesanos.models import Artesano, Emprendimiento, Stand


@admin.register(Artesano)
class ArtesanoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'dni', 'correo', 'telefono', 'localidad', 'provincia', 'emprendimiento']
    search_fields = ('nombre', 'apellido', 'dni', 'correo', 'telefono', 'emprendimiento')
    list_filter = ('dni', 'localidad', 'provincia')


@admin.register(Emprendimiento)
class EmprendimientoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'trayectoria', 'observaciones', 'cantidad_productos', 'ubicacion']
    search_fields = ('nombre', 'ubicacion')
    list_filter = ('ubicacion', )


@admin.register(Stand)
class StandAdmin(admin.ModelAdmin):
    list_display = ['numero', 'zona', 'artesano']
    search_fields = ('numero', 'zona', 'artesano')
    list_filter = ('zona', )
