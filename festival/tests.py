from io import StringIO
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import connection, IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.test import TestCase, Client
from django.urls import reverse
from .models import Edicion, Categoria, Votacion, Opcion

class CatalogoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.e1 = Edicion.objects.create(anio=2027, nombre="Edición A")
        cls.e2 = Edicion.objects.create(anio=2026, nombre="Edición B")
        cls.c1 = Categoria.objects.create(edicion=cls.e1, nombre="Categoría A")
        cls.c2 = Categoria.objects.create(edicion=cls.e2, nombre="Categoría B")
        cls.v1 = Votacion.objects.create(categoria=cls.c1, titulo="Votación A")
        cls.v2 = Votacion.objects.create(categoria=cls.c2, titulo="Votación B")
        cls.o1 = Opcion.objects.create(votacion=cls.v1, nombre="Alternativa A")
        cls.o2 = Opcion.objects.create(votacion=cls.v2, nombre="Alternativa B")

    def test_01_motor_mysql_real(self):
        self.assertEqual(connection.vendor, "mysql")
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            self.assertNotIn("MariaDB", cursor.fetchone()[0])

    def test_02_migracion_aplicada(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM django_migrations "
                           "WHERE app='festival' AND name='0001_initial'")
            self.assertEqual(cursor.fetchone()[0], 1)

    def test_03_relaciones_persistidas(self):
        opcion = Opcion.objects.select_related(
            "votacion__categoria__edicion").get(pk=self.o1.pk)
        self.assertEqual(opcion.votacion.categoria.edicion.anio, 2027)

    def test_04_nombre_reutilizable_otra_edicion(self):
        Categoria.objects.create(edicion=self.e2, nombre=self.c1.nombre)
        self.assertEqual(Categoria.objects.filter(nombre=self.c1.nombre).count(), 2)

    def test_05_restriccion_duplicado_categoria(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Categoria.objects.create(edicion=self.e1, nombre=self.c1.nombre)

    def test_06_restriccion_duplicado_opcion(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Opcion.objects.create(votacion=self.v1, nombre=self.o1.nombre)

    def test_07_proteccion_eliminacion(self):
        for obj in (self.e1, self.c1, self.v1):
            with self.assertRaises(ProtectedError):
                obj.delete()

    def test_08_validacion_anio_y_nombre(self):
        for obj in (Edicion(anio=1800, nombre="Ejemplo"),
                    Categoria(edicion=self.e1, nombre="")):
            with self.assertRaises(ValidationError):
                obj.full_clean()

    def test_09_separacion_categorias(self):
        response = self.client.get(reverse("festival:categorias", args=[self.e1.pk]))
        self.assertContains(response, "Categoría A")
        self.assertNotContains(response, "Categoría B")

    def test_10_separacion_opciones(self):
        url = reverse("festival:detalle", args=[self.e1.pk, self.c1.pk, self.v1.pk])
        response = self.client.get(url)
        self.assertContains(response, "Alternativa A")
        self.assertNotContains(response, "Alternativa B")

    def test_11_ruta_incoherente(self):
        self.assertEqual(self.client.get(reverse("festival:votaciones", args=[
            self.e1.pk, self.c2.pk])).status_code, 404)
        self.assertEqual(self.client.get(reverse("festival:detalle", args=[
            self.e1.pk, self.c1.pk, self.v2.pk])).status_code, 404)

    def test_12_inexistente(self):
        self.assertEqual(self.client.get(reverse("festival:categorias", args=[99999])).status_code, 404)

    def test_13_vacios(self):
        self.assertContains(self.client.get(reverse("festival:categorias", args=[
            Edicion.objects.create(anio=2028, nombre="Vacía").pk])), "todavía no tiene categorías")
        c = Categoria.objects.create(edicion=self.e1, nombre="Sin votaciones")
        self.assertContains(self.client.get(reverse("festival:votaciones", args=[
            self.e1.pk, c.pk])), "todavía no tiene votaciones")
        v = Votacion.objects.create(categoria=c, titulo="Sin opciones")
        self.assertContains(self.client.get(reverse("festival:detalle", args=[
            self.e1.pk, c.pk, v.pk])), "todavía no tiene opciones")

    def test_14_demo_idempotente(self):
        call_command("cargar_demo", stdout=StringIO())
        conteos = [m.objects.count() for m in (Edicion, Categoria, Votacion, Opcion)]
        call_command("cargar_demo", stdout=StringIO())
        self.assertEqual(conteos, [m.objects.count() for m in (Edicion, Categoria, Votacion, Opcion)])

    def test_15_admin_crear_editar_ver_publico(self):
        user = get_user_model().objects.create_superuser(username="admin_test")
        self.client.force_login(user)
        url = reverse("admin:festival_opcion_add")
        self.assertEqual(self.client.post(url, {
            "votacion": self.v1.pk, "nombre": "Creada desde Admin",
            "descripcion": "Dato de prueba", "_save": "Guardar",
        }).status_code, 302)
        opcion = Opcion.objects.get(nombre="Creada desde Admin")
        self.client.post(reverse("admin:festival_opcion_change", args=[opcion.pk]), {
            "votacion": self.v1.pk, "nombre": "Editada desde Admin",
            "descripcion": "Modificada", "_save": "Guardar",
        })
        self.client.logout()
        self.assertContains(self.client.get(reverse("festival:detalle", args=[
            self.e1.pk, self.c1.pk, self.v1.pk])), "Editada desde Admin")
