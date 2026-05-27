from django.shortcuts import render, redirect, get_object_or_404
from .forms import PasajeroFormulario
from .models import Pasajero


def home_view(request):
    return render(request, "index.html", {})


def pasajeros(request):
    pasajeros = Pasajero.objects.all()
    data = PasajeroFormulario()

    if request.method == 'POST':
        formulario = PasajeroFormulario(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="pasajeros")  # FIX: redirigir tras guardar
        else:
            # FIX: mostrar el formulario con errores, no uno vacío
            return render(request, "pasajeros.html", {"pasajeros": pasajeros, "form": formulario})

    return render(request, "pasajeros.html", {"pasajeros": pasajeros, "form": data})


def pasajerosEdit(request, id):
    pasajero = get_object_or_404(Pasajero, id=id)
    data = {
        'form': PasajeroFormulario(instance=pasajero)
    }
    if request.method == 'POST':
        formulario = PasajeroFormulario(data=request.POST, instance=pasajero, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="pasajeros")
        else:
            data['form'] = formulario

    return render(request, 'pasajerosEdit.html', data)


def agregar_pasajero(request):
    if request.method == 'POST':
        formulario = PasajeroFormulario(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="pasajeros")
    else:
        formulario = PasajeroFormulario()
    return render(request, 'agregar_pasajero.html', {'form': formulario})


def eliminar_pasajero(request, id):
    pasajero = get_object_or_404(Pasajero, id=id)
    if request.method == 'POST':  # FIX: solo eliminar si es POST
        pasajero.delete()
    return redirect(to="pasajeros")