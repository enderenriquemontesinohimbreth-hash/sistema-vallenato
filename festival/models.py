from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ValidationError

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
    habilitada = models.BooleanField("habilitada para votar", default=False)
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

    def clean(self):
        super().clean()
        if self.pk:
            anterior = type(self).objects.filter(pk=self.pk).values_list("edicion_id", flat=True).first()
            if anterior is not None and anterior != self.edicion_id:
                raise ValidationError({"edicion": "La relación no puede cambiarse. Cree un registro nuevo."})

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                type(self).objects.select_for_update().filter(pk=self.pk).first()
            self.clean()
            return super().save(*args, **kwargs)

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

    def clean(self):
        super().clean()
        if self.pk:
            anterior = type(self).objects.filter(pk=self.pk).values_list("categoria_id", flat=True).first()
            if anterior is not None and anterior != self.categoria_id:
                raise ValidationError({"categoria": "La relación no puede cambiarse. Cree un registro nuevo."})

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                type(self).objects.select_for_update().filter(pk=self.pk).first()
            self.clean()
            return super().save(*args, **kwargs)

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

    def clean(self):
        super().clean()
        if self.pk:
            anterior = type(self).objects.filter(pk=self.pk).values_list("votacion_id", flat=True).first()
            if anterior is not None and anterior != self.votacion_id:
                raise ValidationError({"votacion": "La votación no puede cambiarse. Cree una opción nueva."})

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} | {self.votacion.titulo}"


class Voto(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="votos")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="votos")
    opcion = models.ForeignKey(Opcion, on_delete=models.PROTECT, related_name="votos")
    creado = models.DateTimeField("fecha de registro", auto_now_add=True)

    class Meta:
        ordering = ["-creado", "-pk"]
        constraints = [models.UniqueConstraint(
            fields=["usuario", "categoria"], name="voto_unico_usuario_categoria",
        )]

    @property
    def edicion(self):
        return self.categoria.edicion

    def clean(self):
        super().clean()
        if self.opcion_id and self.categoria_id:
            opcion = Opcion.objects.select_related("votacion").filter(pk=self.opcion_id).first()
            if not opcion or opcion.votacion.categoria_id != self.categoria_id:
                raise ValidationError("La opción no pertenece a esta categoría y edición.")

    def save(self, *args, **kwargs):
        if not self._state.adding:
            raise ValidationError("Los votos registrados no se pueden modificar.")
        with transaction.atomic():
            categoria = Categoria.objects.select_for_update().get(pk=self.categoria_id)
            if not categoria.habilitada:
                raise ValidationError("Esta categoría está cerrada.")
            self.full_clean(validate_unique=False, validate_constraints=False)
            return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario} | {self.categoria} | {self.opcion.nombre}"
