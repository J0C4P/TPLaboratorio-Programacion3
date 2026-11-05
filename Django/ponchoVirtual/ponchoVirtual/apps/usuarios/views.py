from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from ponchoVirtual.apps.artesanos.models import Stand

from django.shortcuts import render
from ponchoVirtual.apps.artesanos.models import Stand







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





def portada(request):
    # Coordenadas exactas centradas en los galpones del Predio Ferial
    pabellones_dict = {
        "Pabellón A: Textiles y Telar": {"lat": -28.4480, "lng": -65.7583, "stands": []},
        "Pabellón B: Cerámica, Madera y Metal": {"lat": -28.4482, "lng": -65.7570, "stands": []},
        "Pabellón C: Gastronomía y Sabores": {"lat": -28.4495, "lng": -65.7573, "stands": []},
        "Pabellón D: Artesanías en Cuero": {"lat": -28.4475, "lng": -65.7576, "stands": []},
    }

    # Traemos todos los stands con su artesano y emprendimiento en vivo
    stands_db = Stand.objects.select_related('artesano__emprendimiento').order_by('numero')

    for st in stands_db:
        zona_texto = (st.zona or "").upper()
        
        # Mapeamos según la letra del pabellón
        if "B" in zona_texto:
            destino = "Pabellón B: Cerámica, Madera y Metal"
        elif "C" in zona_texto:
            destino = "Pabellón C: Gastronomía y Sabores"
        elif "D" in zona_texto:
            destino = "Pabellón D: Artesanías en Cuero"
        else:
            destino = "Pabellón A: Textiles y Telar"

        tiene_artesano = st.artesano is not None
        artesano_nom = f"{st.artesano.nombre_artesano} {st.artesano.apellido}" if tiene_artesano else None
        
        emp_nom = None
        emp_rubro = None
        if tiene_artesano:
            try:
                emp = st.artesano.emprendimiento
                if emp:
                    emp_nom = emp.nombre_emprendimiento
                    emp_rubro = emp.rubro
            except Exception:
                emp_nom = None

        pabellones_dict[destino]["stands"].append({
            "numero": st.numero,
            "ocupado": tiene_artesano,
            "artesano": artesano_nom,
            "emprendimiento": emp_nom,
            "rubro": emp_rubro
        })

    # Pasamos el diccionario directo (Django se encarga de serializarlo en el template)
    contexto = {
        "datos_mapa": pabellones_dict,
    }
    return render(request, "base/portada.html", contexto)




