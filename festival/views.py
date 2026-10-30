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


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from .forms import SeleccionForm, ConfirmacionForm
from .models import Opcion, Voto
from .services import registrar_voto, VotoDuplicado


def _categoria(edicion_id, categoria_id):
    return get_object_or_404(Categoria.objects.select_related("edicion"),
                             pk=categoria_id, edicion_id=edicion_id)


@login_required
@require_http_methods(["GET", "POST"])
def elegir(request, edicion_id, categoria_id):
    categoria = _categoria(edicion_id, categoria_id)
    if Voto.objects.filter(usuario=request.user, categoria=categoria).exists():
        messages.info(request, "Ya registraste tu voto en esta categoría.")
        return redirect("festival:participacion")
    form = SeleccionForm(request.POST or None, categoria=categoria)
    if not categoria.habilitada:
        return render(request, "festival/elegir.html", {"categoria": categoria, "form": form,
                      "cerrada": True}, status=403)
    if request.method == "POST" and form.is_valid():
        opcion = form.cleaned_data["opcion"]
        return render(request, "festival/confirmar.html", {"categoria": categoria, "opcion": opcion,
                      "form": ConfirmacionForm(categoria=categoria, initial={"opcion": opcion})})
    return render(request, "festival/elegir.html", {"categoria": categoria, "form": form},
                  status=400 if request.method == "POST" else 200)


@login_required
@require_POST
def confirmar(request, edicion_id, categoria_id):
    categoria = _categoria(edicion_id, categoria_id)
    form = ConfirmacionForm(request.POST, categoria=categoria)
    if not form.is_valid():
        return render(request, "festival/elegir.html", {"categoria": categoria, "form": form}, status=400)
    try:
        registrar_voto(usuario=request.user, categoria_id=categoria.pk,
                       opcion_id=form.cleaned_data["opcion"].pk)
    except VotoDuplicado as error:
        messages.info(request, str(error))
    except ValidationError as error:
        form.add_error(None, error)
        return render(request, "festival/elegir.html", {"categoria": categoria, "form": form}, status=400)
    else:
        messages.success(request, "Tu voto quedó registrado correctamente.")
    return redirect("festival:participacion")


@login_required
@require_GET
def participacion(request):
    votos = Voto.objects.filter(usuario=request.user).select_related(
        "categoria__edicion", "opcion__votacion")
    return render(request, "festival/participacion.html", {"votos": votos})


@require_GET
def api_categorias(request):
    categorias = Categoria.objects.select_related("edicion").prefetch_related("votaciones__opciones")
    datos = [{"id": c.pk, "nombre": c.nombre, "habilitada": c.habilitada,
              "edicion": {"id": c.edicion_id, "anio": c.edicion.anio, "nombre": c.edicion.nombre},
              "opciones": [{"id": o.pk, "nombre": o.nombre,
                            "votacion": {"id": v.pk, "titulo": v.titulo}}
                           for v in c.votaciones.all() for o in v.opciones.all()]}
             for c in categorias]
    return JsonResponse({"categorias": datos}, json_dumps_params={"ensure_ascii": False})
