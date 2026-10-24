from django.urls import path
from ponchoVirtual.apps.artesanos.views import solicitud_artesano, datos_artesano, modificar_datos_art, \
    reporte_artesanos_pdf, reporte_artesanos_localidad_pdf, reporte_stands_pdf

app_name = 'artesano'

urlpatterns = [
    path('solicitud/', solicitud_artesano, name='solicitud_artesano'),
    path("artesano/<int:dni_artesano>", datos_artesano, name="datos_artesano"),
    path("modificar_artesano/<int:dni_artesano>", modificar_datos_art, name="modificar_datos_art"),
    path("reporte/registrados", reporte_artesanos_pdf, name="reporte_artesanos_pdf"),
    path("reporte/por_localidad", reporte_artesanos_localidad_pdf, name="reporte_artesanos_localidad_pdf"),
    path("reporte/stands", reporte_stands_pdf, name="reporte_stands_pdf")
]
