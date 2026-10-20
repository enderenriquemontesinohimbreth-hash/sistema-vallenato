from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Edicion(models.Model):
    anio = models.PositiveSmallIntegerField(
        "año", unique=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2200)],
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField("descripción", blank=True)

    class Meta:
        ordering = ["-anio"]
        verbose_name = "edición"
        verbose_name_plural = "ediciones"
        constraints = [models.CheckConstraint(
            condition=models.Q(anio__gte=1900, anio__lte=2200),
            name="edicion_anio_rango",
        )]

    def __str__(self):
        return f"{self.anio} | {self.nombre}"

class Categoria(models.Model):
    edicion = models.ForeignKey(
        Edicion, on_delete=models.PROTECT, related_name="categorias",
        verbose_name="edición",
    )
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField("descripción", blank=True)

    class Meta:
        ordering = ["nombre", "pk"]
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        constraints = [models.UniqueConstraint(
            fields=["edicion", "nombre"], name="categoria_nombre_edicion",
        )]

    def __str__(self):
        return f"{self.edicion.anio} | {self.nombre}"

class Votacion(models.Model):
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="votaciones",
        verbose_name="categoría",
    )
    titulo = models.CharField("título", max_length=150)
    descripcion = models.TextField("descripción", blank=True)

    class Meta:
        ordering = ["titulo", "pk"]
        verbose_name = "votación"
        verbose_name_plural = "votaciones"
        constraints = [models.UniqueConstraint(
            fields=["categoria", "titulo"], name="votacion_titulo_categoria",
        )]

    def __str__(self):
        return f"{self.categoria} | {self.titulo}"

class Opcion(models.Model):
    votacion = models.ForeignKey(
        Votacion, on_delete=models.PROTECT, related_name="opciones",
        verbose_name="votación",
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField("descripción", blank=True)

    class Meta:
        ordering = ["nombre", "pk"]
        verbose_name = "opción"
        verbose_name_plural = "opciones"
        constraints = [models.UniqueConstraint(
            fields=["votacion", "nombre"], name="opcion_nombre_votacion",
        )]

    def __str__(self):
        return f"{self.nombre} | {self.votacion.titulo}"
