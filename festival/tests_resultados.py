from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Categoria, Edicion, Opcion, Votacion, Voto
from .services import registrar_voto, VotoDuplicado


class ResultadosTests(TestCase):
    def setUp(self):
        self.url = reverse("festival:resultados")
        self.e = Edicion.objects.create(anio=2027, nombre="Edición de prueba")
        self.c = Categoria.objects.create(edicion=self.e, nombre="Categoría de prueba", habilitada=True)
        v = Votacion.objects.create(categoria=self.c, titulo="Subevento A")
        v2 = Votacion.objects.create(categoria=self.c, titulo="Subevento B")
        self.o1 = Opcion.objects.create(votacion=v, nombre="Opción con votos")
        self.o2 = Opcion.objects.create(votacion=v2, nombre="Opción sin votos")
        self.u = get_user_model().objects.create_user(username="cuenta_privada_resultados")
        registrar_voto(usuario=self.u, categoria_id=self.c.pk, opcion_id=self.o1.pk)

    def consultar(self, **extra):
        return self.client.get(self.url, {"edicion": self.e.pk, **extra})

    def test_publica_conteos_y_ceros_sin_datos_personales(self):
        r = self.consultar()
        self.assertEqual(r.status_code, 200)
        resumen = r.context["resumenes"][0]
        self.assertEqual(resumen["total"], 1)
        self.assertEqual({o.pk: o.total_votos for o in resumen["opciones"]}, {self.o1.pk: 1, self.o2.pk: 0})
        self.assertContains(r, self.o2.nombre)
        self.assertNotContains(r, self.u.username)
        self.assertIn("no-store", r["Cache-Control"])

    def test_separa_ediciones_y_categorias(self):
        e2 = Edicion.objects.create(anio=2028, nombre="Otra edición")
        c2 = Categoria.objects.create(edicion=e2, nombre="Solo 2028")
        v2 = Votacion.objects.create(categoria=c2, titulo="Solo otro año")
        Opcion.objects.create(votacion=v2, nombre="Opción de otro año")
        otra = Categoria.objects.create(edicion=self.e, nombre="Otra categoría", habilitada=True)
        v3 = Votacion.objects.create(categoria=otra, titulo="Otro subevento")
        o3 = Opcion.objects.create(votacion=v3, nombre="Opción de otra categoría")
        registrar_voto(usuario=self.u, categoria_id=otra.pk, opcion_id=o3.pk)
        r = self.consultar(categoria=self.c.pk)
        self.assertEqual(r.context["total_votos"], 1)
        self.assertNotContains(r, "Opción de otra categoría")
        self.assertNotContains(r, "Opción de otro año")
        self.assertEqual(self.consultar().context["total_votos"], 2)

    def test_identificadores_incoherentes_invalidos_e_inexistentes(self):
        e2 = Edicion.objects.create(anio=2028, nombre="Otra")
        c2 = Categoria.objects.create(edicion=e2, nombre="Categoría ajena")
        self.assertEqual(self.consultar(categoria=c2.pk).status_code, 404)
        self.assertEqual(self.consultar(categoria=999999).status_code, 404)
        self.assertEqual(self.client.get(self.url, {"edicion": 999999}).status_code, 404)
        self.assertEqual(self.client.get(self.url, {"edicion": "texto"}).status_code, 400)
        self.assertEqual(self.client.get(self.url, {"categoria": self.c.pk}).status_code, 400)
        self.assertEqual(self.client.get(self.url, {"edicion": "9" * 40}).status_code, 400)

    def test_cerrada_conserva_resultados(self):
        self.c.habilitada = False
        self.c.save()
        r = self.consultar()
        self.assertEqual(r.context["total_votos"], 1)
        self.assertContains(r, "Cerrada para votar")

    def test_actualiza_tras_otro_voto_y_no_suma_duplicados(self):
        u2 = get_user_model().objects.create_user(username="segundo_votante")
        self.assertEqual(self.consultar().context["total_votos"], 1)
        registrar_voto(usuario=u2, categoria_id=self.c.pk, opcion_id=self.o2.pk)
        self.assertEqual(self.consultar().context["total_votos"], 2)
        with self.assertRaises(VotoDuplicado):
            registrar_voto(usuario=u2, categoria_id=self.c.pk, opcion_id=self.o1.pk)
        self.assertEqual(self.consultar().context["total_votos"], 2)

    def test_consulta_no_escribe_y_post_no_permitido(self):
        antes = Voto.objects.count()
        self.consultar()
        self.assertEqual(self.client.post(self.url, {}).status_code, 405)
        self.assertEqual(Voto.objects.count(), antes)

    def test_estados_vacios(self):
        e2 = Edicion.objects.create(anio=2028, nombre="Vacía")
        r = self.client.get(self.url, {"edicion": e2.pk})
        self.assertContains(r, "Esta edición todavía no tiene categorías")
        c2 = Categoria.objects.create(edicion=e2, nombre="Sin opciones")
        r = self.client.get(self.url, {"edicion": e2.pk})
        self.assertContains(r, "Esta categoría todavía no tiene opciones")
        v2 = Votacion.objects.create(categoria=c2, titulo="Sin votos")
        Opcion.objects.create(votacion=v2, nombre="Cero votos")
        r = self.client.get(self.url, {"edicion": e2.pk})
        self.assertContains(r, "Esta categoría todavía no tiene votos")
        # Otro caso con base vacía, tras borrar las relaciones en orden.
        Voto.objects.all().delete()
        Opcion.objects.all().delete()
        Votacion.objects.all().delete()
        Categoria.objects.all().delete()
        Edicion.objects.all().delete()
        self.assertContains(self.client.get(self.url), "Todavía no hay ediciones disponibles")
