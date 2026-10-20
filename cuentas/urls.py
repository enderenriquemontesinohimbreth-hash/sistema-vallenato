from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import registro
urlpatterns = [
    path("registro/", registro, name="registro"),
    path("ingresar/", LoginView.as_view(), name="login"),
    path("salir/", LogoutView.as_view(), name="logout"),
]
