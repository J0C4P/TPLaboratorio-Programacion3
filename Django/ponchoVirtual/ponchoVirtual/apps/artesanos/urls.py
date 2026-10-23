from django.urls import path
from ponchoVirtual.apps.artesanos.views import solicitud_artesano, datos_artesano, modificar_datos_art

app_name = 'artesano'

urlpatterns = [
    path('solicitud/', solicitud_artesano, name='solicitud_artesano'),
    path("artesano/<int:dni_artesano>", datos_artesano, name="datos_artesano"),
    path("modificar_artesano/<int:dni_artesano>", modificar_datos_art, name="modificar_datos_art")
]
