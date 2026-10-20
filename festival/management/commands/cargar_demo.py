from django.core.management.base import BaseCommand
from django.db import transaction
from festival.models import Categoria, Edicion, Opcion, Votacion

class Command(BaseCommand):
    help = "Carga ejemplos ficticios sin sobrescribir registros existentes."

    @transaction.atomic
    def handle(self, *args, **options):
        for anio in (2026, 2027):
            edicion, _ = Edicion.objects.get_or_create(
                anio=anio, defaults={
                    "nombre": f"Edición de prueba {anio}",
                    "descripcion": "Ejemplo académico. No es información oficial.",
                },
            )
            for nombre in ("Muestra instrumental", "Creación de ejemplo"):
                categoria, _ = Categoria.objects.get_or_create(
                    edicion=edicion, nombre=nombre,
                    defaults={"descripcion": "Categoría ficticia de demostración."},
                )
                votacion, _ = Votacion.objects.get_or_create(
                    categoria=categoria, titulo=f"Muestra {nombre.lower()}",
                    defaults={"descripcion": "Catálogo de prueba sin emisión de votos."},
                )
                for letra in ("A", "B"):
                    Opcion.objects.get_or_create(
                        votacion=votacion, nombre=f"Alternativa {letra}",
                        defaults={"descripcion": "Participante ficticio."},
                    )
        self.stdout.write(self.style.SUCCESS(
            "Carga lista. Catálogo de ejemplo: 2 ediciones, 4 categorías, "
            "4 votaciones y 8 opciones en una base vacía."
        ))
