from django.urls import path
from . import views
app_name = "festival"
urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("ediciones/", views.ediciones, name="ediciones"),
    path("ediciones/<int:edicion_id>/", views.categorias, name="categorias"),
    path("ediciones/<int:edicion_id>/categorias/<int:categoria_id>/",
         views.votaciones, name="votaciones"),
    path("ediciones/<int:edicion_id>/categorias/<int:categoria_id>/"
         "votaciones/<int:votacion_id>/", views.detalle, name="detalle"),
]
