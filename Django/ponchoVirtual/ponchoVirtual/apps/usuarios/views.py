from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from ponchoVirtual.apps.artesanos.models import Artesano, Stand
from ponchoVirtual.apps.usuarios.forms import StandForm
from ponchoVirtual.apps.usuarios.models import Usuario


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


@login_required(login_url='usuario:login')
@permission_required('artesanos.view_stand', raise_exception=True)
def gestion_stands(request):
    stands = Stand.objects.select_related('artesano').order_by('zona', 'numero')
    dnis_aprobados = Usuario.objects.filter(is_active=True).values('documento_identidad')
    artesanos_sin_stand = Artesano.objects.filter(stand__isnull=True, dni__in=dnis_aprobados)
    ocupados = sum(1 for s in stands if s.artesano_id)
    contexto = {
        'stands': stands,
        'artesanos_sin_stand': artesanos_sin_stand,
        'total': len(stands),
        'ocupados': ocupados,
        'disponibles': len(stands) - ocupados,
    }
    return render(request, 'gestion_stands.html', contexto)


@login_required(login_url='usuario:login')
@permission_required('artesanos.add_stand', raise_exception=True)
def crear_stand(request):
    if request.method == "POST":
        form = StandForm(request.POST)
        if form.is_valid():
            stand = form.save()
            messages.success(request, f'Se creó el {stand}.')
            return redirect('usuario:gestion_stands')
    else:
        form = StandForm()
    return render(request, 'crear_stand.html', {'form': form})


@login_required(login_url='usuario:login')
@permission_required('artesanos.change_stand', raise_exception=True)
@require_POST
def asignar_stand(request, id_stand):
    stand = get_object_or_404(Stand, id=id_stand)
    artesano = get_object_or_404(Artesano, id=request.POST.get('artesano'))

    if stand.artesano_id:
        messages.error(request, f'El {stand} ya está ocupado. Libéralo antes de asignarlo.')
    elif Stand.objects.filter(artesano=artesano).exists():
        messages.error(request, f'{artesano} ya tiene un stand asignado.')
    else:
        stand.artesano = artesano
        stand.save()
        messages.success(request, f'{artesano} fue asignado al {stand}.')
    return redirect('usuario:gestion_stands')


@login_required(login_url='usuario:login')
@permission_required('artesanos.change_stand', raise_exception=True)
@require_POST
def liberar_stand(request, id_stand):
    stand = get_object_or_404(Stand, id=id_stand)
    if stand.artesano_id:
        stand.artesano = None
        stand.save()
        messages.success(request, f'El {stand} fue liberado.')
    else:
        messages.info(request, f'El {stand} ya estaba disponible.')
    return redirect('usuario:gestion_stands')
