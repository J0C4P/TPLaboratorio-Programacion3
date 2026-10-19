from django.urls import path
from ponchoVirtual.apps.artesanos.views import solicitud_artesano

app_name = 'artesano'

urlpatterns = [
    path('solicitud/', solicitud_artesano, name='solicitud_artesano'),
]
