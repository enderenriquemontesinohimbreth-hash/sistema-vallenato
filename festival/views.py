from django.shortcuts import get_object_or_404, render
from .models import Categoria, Edicion, Votacion

def inicio(request):
    return render(request, "festival/inicio.html", {
        "ediciones": Edicion.objects.all()[:3],
    })

def ediciones(request):
    return render(request, "festival/ediciones.html", {
        "ediciones": Edicion.objects.all(),
    })

def categorias(request, edicion_id):
    edicion = get_object_or_404(Edicion, pk=edicion_id)
    return render(request, "festival/categorias.html", {
        "edicion": edicion, "categorias": edicion.categorias.all(),
    })

def votaciones(request, edicion_id, categoria_id):
    categoria = get_object_or_404(
        Categoria.objects.select_related("edicion"),
        pk=categoria_id, edicion_id=edicion_id,
    )
    return render(request, "festival/votaciones.html", {
        "categoria": categoria, "votaciones": categoria.votaciones.all(),
    })

def detalle(request, edicion_id, categoria_id, votacion_id):
    votacion = get_object_or_404(
        Votacion.objects.select_related("categoria__edicion"),
        pk=votacion_id, categoria_id=categoria_id,
        categoria__edicion_id=edicion_id,
    )
    return render(request, "festival/detalle.html", {
        "votacion": votacion, "opciones": votacion.opciones.all(),
    })
