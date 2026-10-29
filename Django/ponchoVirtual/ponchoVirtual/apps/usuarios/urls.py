from django.urls import path
from ponchoVirtual.apps.usuarios.views import login_vista, logout_vista, gestion_stands, crear_stand, asignar_stand, \
    liberar_stand

app_name = 'usuario'

urlpatterns = [
    path('login', login_vista, name="login"),
    path('logout', logout_vista, name="logout"),
    path('panel/stands/', gestion_stands, name="gestion_stands"),
    path('panel/stands/nuevo/', crear_stand, name="crear_stand"),
    path('panel/stands/<int:id_stand>/asignar/', asignar_stand, name="asignar_stand"),
    path('panel/stands/<int:id_stand>/liberar/', liberar_stand, name="liberar_stand"),
]
