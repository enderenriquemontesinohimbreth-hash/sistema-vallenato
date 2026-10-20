from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import RegistroForm

def registro(request):
    if request.user.is_authenticated:
        return redirect("festival:inicio")
    form = RegistroForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Cuenta creada. Ya puedes iniciar sesión.")
        return redirect("login")
    return render(request, "registration/registro.html", {"form": form})
