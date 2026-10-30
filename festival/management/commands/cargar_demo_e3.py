from django.core.management.base import BaseCommand
from django.db import transaction
from festival.models import Edicion, Categoria, Votacion, Opcion


class Command(BaseCommand):
    help = "Agrega ejemplos E3 sin borrar datos, votos ni crear contraseñas. Solo desarrollo."

    @transaction.atomic
    def handle(self, *args, **options):
        for anio in [2027, 2026]:
            edicion, _ = Edicion.objects.get_or_create(anio=anio, defaults={"nombre": f"Edición de prueba {anio}"})
            for nombre, habilitada in [("Ejemplo E3: acordeón", True), ("Ejemplo E3: canción", True),
                                       ("Ejemplo E3: cerrada", False), ("Ejemplo E3: sin opciones", True)]:
                categoria, _ = Categoria.objects.get_or_create(edicion=edicion, nombre=nombre,
                    defaults={"habilitada": habilitada, "descripcion": "Dato ficticio de demostración."})
                if "sin opciones" in nombre:
                    continue
                for n in [1, 2]:
                    votacion, _ = Votacion.objects.get_or_create(categoria=categoria, titulo=f"Subevento de ejemplo {n}")
                    for letra in ["A", "B"]:
                        Opcion.objects.get_or_create(votacion=votacion, nombre=f"Ejemplo {n}-{letra}",
                            defaults={"descripcion": "Opción ficticia; no es un participante oficial."})
        self.stdout.write(self.style.SUCCESS("Ejemplos E3 disponibles. No se sobrescribieron estados existentes ni votos."))
