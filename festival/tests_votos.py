from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import connections, close_old_connections, transaction, IntegrityError
from django.test import TestCase, TransactionTestCase, Client
from django.urls import reverse
from .models import Edicion, Categoria, Votacion, Opcion, Voto
from .services import registrar_voto, VotoDuplicado


def datos():
    e = Edicion.objects.create(anio=2027, nombre="Prueba E3")
    c = Categoria.objects.create(edicion=e, nombre="Categoría A", habilitada=True)
    otra = Categoria.objects.create(edicion=e, nombre="Categoría B", habilitada=True)
    v = Votacion.objects.create(categoria=c, titulo="Subevento A")
    v2 = Votacion.objects.create(categoria=c, titulo="Subevento B")
    v3 = Votacion.objects.create(categoria=otra, titulo="Subevento C")
    o = Opcion.objects.create(votacion=v, nombre="Opción A")
    o2 = Opcion.objects.create(votacion=v2, nombre="Opción B")
    o3 = Opcion.objects.create(votacion=v3, nombre="Opción C")
    u = get_user_model().objects.create_user(username="participante_e3", password="ClaveSoloPruebas_E3!")
    return e, c, otra, o, o2, o3, u


class VotacionesTests(TestCase):
    def setUp(self):
        self.e, self.c, self.otra, self.o, self.o2, self.o3, self.u = datos()
        self.client.force_login(self.u)
        self.url = reverse("festival:confirmar", args=[self.e.pk, self.c.pk])
        self.elegir = reverse("festival:elegir", args=[self.e.pk, self.c.pk])

    def votar(self, opcion=None):
        return self.client.post(self.url, {"opcion": (opcion or self.o).pk, "confirmar": "on"})

    def test_cp01_confirmacion_y_persistencia(self):
        r = self.client.post(self.elegir, {"opcion": self.o.pk})
        self.assertContains(r, "Confirma tu voto")
        self.assertEqual(Voto.objects.count(), 0)
        self.assertRedirects(self.votar(), reverse("festival:participacion"))
        self.assertEqual(Voto.objects.get().opcion_id, self.o.pk)

    def test_cp02_duplicado_otro_subevento(self):
        self.votar()
        self.assertRedirects(self.votar(self.o2), reverse("festival:participacion"))
        self.assertEqual(Voto.objects.count(), 1)
        with self.assertRaises(VotoDuplicado):
            registrar_voto(usuario=self.u, categoria_id=self.c.pk, opcion_id=self.o2.pk)

    def test_cp03_otra_categoria(self):
        self.votar()
        registrar_voto(usuario=self.u, categoria_id=self.otra.pk, opcion_id=self.o3.pk)
        self.assertEqual(Voto.objects.count(), 2)

    def test_cp04_sin_sesion(self):
        self.client.logout()
        self.assertEqual(self.votar().status_code, 302)
        self.assertEqual(Voto.objects.count(), 0)

    def test_cp05_cerrada_entre_seleccion_y_confirmacion(self):
        self.client.post(self.elegir, {"opcion": self.o.pk})
        self.c.habilitada = False
        self.c.save()
        self.assertEqual(self.votar().status_code, 400)
        self.assertEqual(Voto.objects.count(), 0)
        self.assertEqual(self.client.get(self.elegir).status_code, 403)

    def test_cp06_opcion_ajena(self):
        self.assertEqual(self.votar(self.o3).status_code, 400)
        self.assertEqual(Voto.objects.count(), 0)
        with self.assertRaises(ValidationError):
            Voto.objects.create(usuario=self.u, categoria=self.c, opcion=self.o3)

    def test_cp07_historial_personal(self):
        self.votar()
        self.assertContains(self.client.get(reverse("festival:participacion")), "Opción A")
        otro = get_user_model().objects.create_user(username="otro")
        self.client.force_login(otro)
        self.assertNotContains(self.client.get(reverse("festival:participacion")), "Opción A")

    def test_cp08_admin_solo_consulta(self):
        self.votar()
        admin = get_user_model().objects.create_superuser(username="admin_e3")
        self.client.force_login(admin)
        self.assertContains(self.client.get(reverse("admin:festival_voto_changelist")), "Opción A")
        self.assertEqual(self.client.post(reverse("admin:festival_voto_add"), {}).status_code, 403)
        self.assertEqual(self.client.post(reverse("admin:festival_voto_delete", args=[Voto.objects.get().pk]), {}).status_code, 403)

    def test_cp10_api_mysql_y_vacios(self):
        Categoria.objects.create(edicion=self.e, nombre="Vacía")
        r = self.client.get(reverse("festival:api_categorias"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r["Content-Type"], "application/json")
        d = r.json()["categorias"]
        a = next(c for c in d if c["id"] == self.c.pk)
        self.assertEqual({o["id"] for o in a["opciones"]}, {self.o.pk, self.o2.pk})
        self.assertEqual(next(c for c in d if c["nombre"] == "Vacía")["opciones"], [])
        self.assertEqual(self.client.post(reverse("festival:api_categorias"), {}).status_code, 405)

    def test_get_no_vota_y_csrf(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)
        self.assertEqual(Voto.objects.count(), 0)
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.u)
        self.assertEqual(cliente.post(self.url, {"opcion": self.o.pk, "confirmar": "on"}).status_code, 403)

    def test_edicion_incoherente_y_confirmacion_ausente(self):
        url = reverse("festival:confirmar", args=[99999, self.c.pk])
        self.assertEqual(self.client.post(url, {"opcion": self.o.pk, "confirmar": "on"}).status_code, 404)
        self.assertEqual(self.client.post(self.url, {"opcion": self.o.pk}).status_code, 400)
        self.assertEqual(Voto.objects.count(), 0)

    def test_constraint_mysql_directa(self):
        self.votar()
        # bulk_create omite save(): comprueba la restricción SQL independientemente del servicio.
        with self.assertRaises(IntegrityError), transaction.atomic():
            Voto.objects.bulk_create([Voto(usuario=self.u, categoria=self.c, opcion=self.o2)])

    def test_voto_inmutable_y_relaciones_inmutables(self):
        self.votar()
        voto = Voto.objects.get()
        voto.opcion = self.o2
        with self.assertRaises(ValidationError):
            voto.save()
        self.o.votacion = self.o3.votacion
        with self.assertRaises(ValidationError):
            self.o.save()
        self.c.edicion = Edicion.objects.create(anio=2028, nombre="Otra edición")
        with self.assertRaises(ValidationError):
            self.c.save()

    def test_edicion_distinta_permite_participar(self):
        self.votar()
        e = Edicion.objects.create(anio=2028, nombre="Otra")
        c = Categoria.objects.create(edicion=e, nombre=self.c.nombre, habilitada=True)
        v = Votacion.objects.create(categoria=c, titulo="Otro")
        o = Opcion.objects.create(votacion=v, nombre="Otra")
        registrar_voto(usuario=self.u, categoria_id=c.pk, opcion_id=o.pk)
        self.assertEqual(Voto.objects.count(), 2)


class ConcurrenciaTests(TransactionTestCase):
    def test_cp09_dos_post_simultaneos(self):
        self.assertEqual(connections["default"].vendor, "mysql")
        e, c, _, o, o2, _, u = datos()
        url = reverse("festival:confirmar", args=[e.pk, c.pk])
        clientes = [Client(), Client()]
        for cliente in clientes:
            cliente.force_login(u)
        barrera = Barrier(2)

        def enviar(indice):
            close_old_connections()
            try:
                with connections["default"].cursor() as cursor:
                    cursor.execute("SELECT CONNECTION_ID()")
                    conexion = cursor.fetchone()[0]
                barrera.wait(timeout=15)
                r = clientes[indice].post(url, {"opcion": [o.pk, o2.pk][indice], "confirmar": "on"})
                mensajes = [str(m) for m in r.wsgi_request._messages]
                return conexion, r.status_code, mensajes
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as ejecutor:
            resultados = list(ejecutor.map(enviar, [0, 1]))
        self.assertEqual(len({r[0] for r in resultados}), 2)
        self.assertEqual([r[1] for r in resultados], [302, 302])
        self.assertEqual(Voto.objects.filter(usuario=u, categoria=c).count(), 1)
        mensajes = [m for r in resultados for m in r[2]]
        self.assertEqual(sum("correctamente" in m for m in mensajes), 1)
        self.assertEqual(sum("Ya registraste" in m for m in mensajes), 1)
