from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UsuarioForm


def login_vista(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('principal')
        else:
            return render(request, 'login.html', {"msj": "Credenciales incorrectas"})
    # GET
    else:
        return render(request, 'login.html')


def logout_vista(request):
    logout(request)
    return redirect('principal')


def crear_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Se ha ingresado correctamente el usuario")
            return redirect('usuario:login')
    else:
        form = UsuarioForm()
    return render(request, 'crear_usuario.html', {'form': form})
