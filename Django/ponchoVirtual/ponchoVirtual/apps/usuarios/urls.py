from django.urls import path
from ponchoVirtual.apps.usuarios.views import login_vista, logout_vista, crear_usuario

app_name = 'usuario'

urlpatterns = [
    path('login', login_vista, name="login"),
    path('logout', logout_vista, name="logout"),
    path('nuevo_usuario', crear_usuario, name="crear_usuario")
]
