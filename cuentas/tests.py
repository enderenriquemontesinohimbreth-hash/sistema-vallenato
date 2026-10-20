from secrets import token_urlsafe
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

class CuentaTests(TestCase):
    def setUp(self):
        self.password = token_urlsafe(24)
        self.data = {"username": "participante_prueba", "password1": self.password,
                     "password2": self.password}

    def test_16_registro_valido_sin_privilegios(self):
        self.assertRedirects(self.client.post(reverse("registro"), self.data), reverse("login"))
        user = get_user_model().objects.get(username=self.data["username"])
        self.assertTrue(user.check_password(self.password))
        self.assertNotEqual(user.password, self.password)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_17_registro_duplicado(self):
        self.client.post(reverse("registro"), self.data)
        response = self.client.post(reverse("registro"), self.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_18_registro_invalido(self):
        for data in ({}, {**self.data, "password2": "diferente"},
                     {**self.data, "password1": "123", "password2": "123"}):
            response = self.client.post(reverse("registro"), data)
            self.assertTrue(response.context["form"].errors)
        self.assertEqual(get_user_model().objects.count(), 0)

    def test_19_login_valido_invalido(self):
        get_user_model().objects.create_user(self.data["username"], password=self.password)
        self.client.post(reverse("login"), {"username": self.data["username"], "password": "incorrecta"})
        self.assertNotIn("_auth_user_id", self.client.session)
        self.client.post(reverse("login"), {"username": self.data["username"], "password": self.password})
        self.assertIn("_auth_user_id", self.client.session)

    def test_20_logout_post_y_no_get(self):
        user = get_user_model().objects.create_user("temporal")
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.assertIn("_auth_user_id", self.client.session)
        self.assertRedirects(self.client.post(reverse("logout")), reverse("festival:inicio"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_21_csrf_exigido(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post(reverse("registro"), self.data).status_code, 403)
        self.assertEqual(client.post(reverse("login"), {}).status_code, 403)
        user = get_user_model().objects.create_user("csrf_test")
        client.force_login(user)
        self.assertEqual(client.post(reverse("logout")).status_code, 403)

    def test_22_admin_no_disponible_para_participante(self):
        self.assertEqual(self.client.get(reverse("admin:index")).status_code, 302)
        user = get_user_model().objects.create_user("normal")
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("admin:index")).status_code, 302)
        self.assertEqual(self.client.get(reverse("admin:festival_edicion_add")).status_code, 302)

    def test_23_next_externo_no_redirige(self):
        get_user_model().objects.create_user(self.data["username"], password=self.password)
        response = self.client.post(reverse("login"), {
            "username": self.data["username"], "password": self.password,
            "next": "https://example.org/no-autorizado",
        })
        self.assertRedirects(response, reverse("festival:inicio"))

    def test_24_next_local_admitido(self):
        get_user_model().objects.create_user(self.data["username"], password=self.password)
        response = self.client.post(reverse("login"), {
            "username": self.data["username"], "password": self.password,
            "next": reverse("festival:ediciones"),
        })
        self.assertRedirects(response, reverse("festival:ediciones"))
