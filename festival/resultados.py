"""Consulta pública de resultados agregados, sin modificar votos."""
from django.db.models import Count
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET
from .models import Categoria, Edicion, Opcion


def _identificador(valor):
    # Evita ValueError y números desmesurados enviados por URL.
    if not valor or not valor.isascii() or not valor.isdecimal() or len(valor) > 18:
        raise ValueError
    numero = int(valor)
    if numero <= 0:
        raise ValueError
    return numero


@require_GET
@never_cache
def resultados(request):
    ediciones = list(Edicion.objects.all())
    valor_edicion = request.GET.get("edicion", "")
    valor_categoria = request.GET.get("categoria", "")
    try:
        edicion_id = _identificador(valor_edicion) if valor_edicion else None
        categoria_id = _identificador(valor_categoria) if valor_categoria else None
    except ValueError:
        return HttpResponseBadRequest("Selecciona identificadores válidos de edición y categoría.")
    if categoria_id and not edicion_id:
        return HttpResponseBadRequest("Selecciona la edición antes de filtrar una categoría.")
    edicion = (get_object_or_404(Edicion, pk=edicion_id) if edicion_id
               else (ediciones[0] if ediciones else None))
    categorias = list(Categoria.objects.filter(edicion=edicion)) if edicion else []
    if categoria_id:
        categoria = get_object_or_404(Categoria, pk=categoria_id, edicion=edicion)
        seleccionadas = [categoria]
    else:
        seleccionadas = categorias
    resumenes = [{"categoria": c, "opciones": [], "total": 0} for c in seleccionadas]
    por_categoria = {r["categoria"].pk: r for r in resumenes}
    if por_categoria:
        # LEFT JOIN desde Opcion conserva opciones con cero votos.
        opciones = (Opcion.objects.filter(votacion__categoria_id__in=por_categoria)
                    .select_related("votacion")
                    .annotate(total_votos=Count("votos"))
                    .order_by("votacion__categoria_id", "-total_votos", "nombre", "pk"))
        for opcion in opciones:
            resumen = por_categoria[opcion.votacion.categoria_id]
            resumen["opciones"].append(opcion)
            resumen["total"] += opcion.total_votos
    return render(request, "festival/resultados.html", {
        "ediciones": ediciones, "edicion": edicion, "categorias": categorias,
        "categoria_id": categoria_id, "resumenes": resumenes,
        "total_votos": sum(r["total"] for r in resumenes),
    })
