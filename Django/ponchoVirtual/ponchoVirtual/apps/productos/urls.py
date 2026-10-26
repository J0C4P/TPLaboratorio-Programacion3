from django.urls import path
from ponchoVirtual.apps.productos.views import ver_productos_artesano, ver_mis_productos, listar_productos, agregar_productos, detalles_producto, \
    modificar_producto, eliminar_producto, reporte_productos_artesano_pdf, reporte_artesanos_rubro_pdf

app_name = "productos"

urlpatterns = [
    path("", listar_productos, name="listar_productos"),
    path("ver_productos_artesano/<str:artesano_dni>", ver_productos_artesano, name="ver_productos_artesano"),
    path("ver_mis_productos/<str:artesano_dni>", ver_mis_productos, name="ver_mis_productos"),
    path("agregar_producto/", agregar_productos, name="agregar_productos"),
    path("detalles_producto/<int:id_producto>", detalles_producto, name="detalles_producto"),
    path("modificar_producto/<int:id_producto>", modificar_producto, name="modificar_producto"),
    path("eliminar_producto/<int:id_producto>", eliminar_producto, name="eliminar_producto"),
    path("reporte/mis_productos/<str:artesano_dni>", reporte_productos_artesano_pdf, name="reporte_mis_productos_pdf"),
    path("reporte/por_rubro", reporte_artesanos_rubro_pdf, name="reporte_artesanos_rubro_pdf")
]

