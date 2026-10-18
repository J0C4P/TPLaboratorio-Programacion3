from django.urls import path
from ponchoVirtual.apps.productos.views import mis_productos

app_name = "productos"

urlpatterns = [path("mis_productos/", mis_productos, name="mis_productos"),]

