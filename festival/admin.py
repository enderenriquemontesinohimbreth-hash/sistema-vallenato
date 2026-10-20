from django.contrib import admin
from .models import Categoria, Edicion, Opcion, Votacion

admin.site.site_header = "Festival | Administración académica"
admin.site.site_title = "Catálogo del Festival"
admin.site.index_title = "Ediciones, categorías, votaciones y opciones"

@admin.register(Edicion)
class EdicionAdmin(admin.ModelAdmin):
    list_display = ("anio", "nombre")
    search_fields = ("nombre",)
    list_filter = ("anio",)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "edicion")
    list_filter = ("edicion",)
    search_fields = ("nombre", "edicion__nombre")
    list_select_related = ("edicion",)

@admin.register(Votacion)
class VotacionAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria")
    list_filter = ("categoria__edicion", "categoria")
    search_fields = ("titulo", "categoria__nombre")
    list_select_related = ("categoria__edicion",)

@admin.register(Opcion)
class OpcionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "votacion")
    list_filter = ("votacion__categoria__edicion", "votacion")
    search_fields = ("nombre", "votacion__titulo")
    list_select_related = ("votacion__categoria__edicion",)
