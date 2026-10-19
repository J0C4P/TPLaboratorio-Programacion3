from django.contrib import messages
from django.shortcuts import render, redirect
from ponchoVirtual.apps.artesanos.forms import ArtesanoForm, EmprendimientoForm
from ponchoVirtual.apps.artesanos.models import Artesano


def solicitud_artesano(request):
    if request.method == "POST":
        form_artesano = ArtesanoForm(request.POST)
        form_emprendimiento = EmprendimientoForm(request.POST)

        if form_artesano.is_valid() and form_emprendimiento.is_valid():
            emprendimiento = form_emprendimiento.save()
            artesano = form_artesano.save(commit=False)

            artesano.emprendimiento = emprendimiento

            artesano.save()
            messages.success(request, "¡Registro completado con éxito!")
            return redirect(request, 'productos:mis_productos')
    else:
        form_artesano = ArtesanoForm()
        form_emprendimiento = EmprendimientoForm()
    return render(request, 'Crear_art_emp.html', {'form_art': form_artesano, 'form_emp': form_emprendimiento})