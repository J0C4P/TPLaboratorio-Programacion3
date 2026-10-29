from django.urls import path
from ponchoVirtual.apps.artesanos.views import (solicitud_artesano, datos_artesano, modificar_datos_art,
                                                reporte_artesanos_pdf, reporte_artesanos_localidad_pdf,
                                                reporte_stands_pdf, solicitudes_artesanos_admin, evaluar_solicitud_admin, consultar_estado_solicitud)

app_name = 'artesano'

urlpatterns = [
    path('solicitud/', solicitud_artesano, name='solicitud_artesano'),
    path("artesano/<int:dni_artesano>", datos_artesano, name="datos_artesano"),
    path("modificar_artesano/<int:dni_artesano>", modificar_datos_art, name="modificar_datos_art"),
    path("reporte/registrados", reporte_artesanos_pdf, name="reporte_artesanos_pdf"),
    path("reporte/por_localidad", reporte_artesanos_localidad_pdf, name="reporte_artesanos_localidad_pdf"),
    path("reporte/stands", reporte_stands_pdf, name="reporte_stands_pdf"),
    path("solicitudes_artesanos", solicitudes_artesanos_admin, name="solicitudes_artesanos_admin"),
    path("evaluar_solicitud_admin/<int:dni>", evaluar_solicitud_admin, name="evaluar_solicitud_admin"),
    path("consultar_estado_solicitud", consultar_estado_solicitud, name="consultar_estado_solicitud")
]
