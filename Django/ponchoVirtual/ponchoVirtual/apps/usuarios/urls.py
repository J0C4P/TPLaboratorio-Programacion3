from django.urls import path
from ponchoVirtual.apps.usuarios.views import login_vista, logout_vista
from usuarios.views import (solicitudes_artesanos_admin, evaluar_solicitud_admin, consultar_estado_solicitud,
                            listar_artesanos_aceptados, solicitudes_rechazadas_admin, reconsiderar_solicitud_admin)

app_name = 'usuario'

urlpatterns = [
    path('login', login_vista, name="login"),
    path('logout', logout_vista, name="logout"),
    path("solicitudes_artesanos", solicitudes_artesanos_admin, name="solicitudes_artesanos_admin"),
    path("evaluar_solicitud_admin/<int:dni>", evaluar_solicitud_admin, name="evaluar_solicitud_admin"),
    path("consultar_estado_solicitud", consultar_estado_solicitud, name="consultar_estado_solicitud"),
    path('administracion/aceptados/', listar_artesanos_aceptados, name='listar_artesanos_aceptados'),
    path('administracion/rechazadas/', solicitudes_rechazadas_admin, name='solicitudes_rechazadas_admin'),
    path('administracion/reconsiderar/<str:dni>/', reconsiderar_solicitud_admin, name='reconsiderar_solicitud_admin'),
]
