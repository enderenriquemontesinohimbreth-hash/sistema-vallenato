from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from .models import Categoria, Opcion, Voto


class VotoDuplicado(Exception):
    pass


def registrar_voto(*, usuario, categoria_id, opcion_id):
    if not usuario.is_authenticated or not usuario.is_active:
        raise ValidationError("Debes iniciar sesión con una cuenta activa.")
    try:
        with transaction.atomic():
            # También serializa el cierre de la categoría mediante Categoria.save().
            categoria = Categoria.objects.select_for_update().get(pk=categoria_id)
            if not categoria.habilitada:
                raise ValidationError("Esta categoría está cerrada.")
            if not Opcion.objects.filter(pk=opcion_id, votacion__categoria=categoria).exists():
                raise ValidationError("La opción no pertenece a esta categoría y edición.")
            if Voto.objects.filter(usuario=usuario, categoria=categoria).exists():
                raise VotoDuplicado("Ya registraste tu voto en esta categoría.")
            return Voto.objects.create(usuario=usuario, categoria=categoria, opcion_id=opcion_id)
    except IntegrityError as error:
        # Capturar fuera de atomic: la conexión ya no está en una transacción rota.
        causa = error.__cause__
        if causa and causa.args and causa.args[0] == 1062 and "voto_unico_usuario_categoria" in str(causa):
            raise VotoDuplicado("Ya registraste tu voto en esta categoría.") from error
        raise
