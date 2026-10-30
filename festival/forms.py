from django import forms
from .models import Opcion


class SeleccionForm(forms.Form):
    opcion = forms.ModelChoiceField(queryset=Opcion.objects.none(), widget=forms.RadioSelect,
                                    label="Elige una sola opción", empty_label=None)

    def __init__(self, *args, categoria, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["opcion"].queryset = Opcion.objects.filter(
            votacion__categoria=categoria).select_related("votacion").order_by("votacion__titulo", "nombre", "pk")


class ConfirmacionForm(SeleccionForm):
    confirmar = forms.BooleanField(label="Confirmo que deseo registrar esta elección")
