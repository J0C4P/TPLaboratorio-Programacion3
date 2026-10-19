from django.urls import path
from ponchoVirtual.apps.productos.views import mis_productos, listar_productos, agregar_productos

app_name = "productos"

urlpatterns = [
    path("", listar_productos, name="listar_productos"),
    path("mis_productos/<str:artesano_dni>", mis_productos, name="mis_productos"),
    path("agregar_producto/", agregar_productos, name="agregar_productos")
]

