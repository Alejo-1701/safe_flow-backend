from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken

from config.test_helpers import ApiTestCaseBase, crear_perfil

from .authentication import PerfilJWTAuthentication


class LoginApiTests(ApiTestCaseBase):
    def test_login_con_password_hasheado(self):
        crear_perfil(contrasenia="Clave123")

        response = self.client.post(
            "/api/usuarios/login/",
            {"num_documento": "10000001", "contrasenia": "Clave123"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["num_documento"], "10000001")
        self.assertEqual(response.data["rol"], "Residente")
        self.assertIn("Ana", response.data["nombre_completo"])
        self.assertIn("Pérez", response.data["nombre_completo"])

    def test_login_con_password_plano_temporal(self):
        crear_perfil(num_documento="10000002", contrasenia="Clave123", hash_contrasenia=False)

        response = self.client.post(
            "/api/usuarios/login/",
            {"num_documento": "10000002", "contrasenia": "Clave123"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_login_contrasenia_incorrecta(self):
        crear_perfil(contrasenia="Clave123")

        response = self.client.post(
            "/api/usuarios/login/",
            {"num_documento": "10000001", "contrasenia": "Incorrecta"},
            format="json",
        )

        self.assertEqual(response.status_code, 401)

    def test_login_perfil_inexistente(self):
        response = self.client.post(
            "/api/usuarios/login/",
            {"num_documento": "99999999", "contrasenia": "Clave123"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_login_perfil_inactivo_devuelve_403(self):
        crear_perfil(num_documento="10000003", contrasenia="Clave123", estado=False)

        response = self.client.post(
            "/api/usuarios/login/",
            {"num_documento": "10000003", "contrasenia": "Clave123"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)


class AutenticacionJwtTests(ApiTestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.perfil = crear_perfil(contrasenia="Clave123")

    def _token_de_acceso(self, num_documento="10000001", rol="Residente"):
        refresh = RefreshToken()
        refresh["user_id"] = num_documento
        refresh["rol"] = rol
        return str(refresh.access_token)

    def test_token_resuelve_perfil_autenticado(self):
        factory = APIRequestFactory()
        request = factory.get(
            "/api/usuarios/perfiles/",
            HTTP_AUTHORIZATION=f"Bearer {self._token_de_acceso()}",
        )

        usuario, _ = PerfilJWTAuthentication().authenticate(request)

        self.assertEqual(usuario.doc_persona_id, "10000001")
        self.assertTrue(usuario.is_authenticated)

    def test_token_de_perfil_inactivo_se_rechaza(self):
        crear_perfil(num_documento="10000004", estado=False)
        factory = APIRequestFactory()
        request = factory.get(
            "/api/usuarios/perfiles/",
            HTTP_AUTHORIZATION=f"Bearer {self._token_de_acceso('10000004')}",
        )

        with self.assertRaises(AuthenticationFailed):
            PerfilJWTAuthentication().authenticate(request)
