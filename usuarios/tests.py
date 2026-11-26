from config.test_helpers import APITestCaseBase
from personas.models import Persona
from rest_framework_simplejwt.tokens import AccessToken
from usuarios.authentication import PerfilJWTAuthentication
from usuarios.models import Perfil

URL = "/api/usuarios/perfiles/"
DOC = "TST001"
CLAVE = "ClaveSegura2026!"
CLAVE_NUEVA = "OtraClaveSegura2026!"


class PerfilCRUDTests(APITestCaseBase):
    def setUp(self):
        Persona.objects.create(
            num_documento=DOC,
            tipo_documento="CC",
            primer_nombre="Soporte",
            primer_apellido="Prueba",
            segundo_apellido="Test",
            id_rol_id=1,
        )

    def datos(self, clave=CLAVE):
        return {"doc_persona": DOC, "contrasenia": clave, "estado_perfil": True}

    def test_ciclo_completo(self):
        self.ciclo_crud(
            {
                "url": URL,
                "pk": "doc_persona",
                "crear": lambda: self.datos(),
                "actualizar": lambda pk: self.datos(CLAVE_NUEVA),
                "parchear": {"estado_perfil": False},
            }
        )

    def test_contrasenia_hasheada_en_creacion(self):
        respuesta = self.client.post(URL, self.datos(), format="json")
        self.assertEqual(respuesta.status_code, 201, respuesta.content)
        perfil = Perfil.objects.get(doc_persona=DOC)
        self.assertTrue(perfil.contrasenia.startswith("pbkdf2_"))
        self.assertNotEqual(perfil.contrasenia, CLAVE)

    def test_contrasenia_hasheada_en_actualizacion(self):
        self.client.post(URL, self.datos(), format="json")
        anterior = Perfil.objects.get(doc_persona=DOC).contrasenia
        respuesta = self.client.put(f"{URL}{DOC}/", self.datos(CLAVE_NUEVA), format="json")
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        actual = Perfil.objects.get(doc_persona=DOC).contrasenia
        self.assertNotEqual(actual, anterior)
        self.assertTrue(actual.startswith("pbkdf2_"))
        self.assertNotEqual(actual, CLAVE_NUEVA)

    def test_contrasenia_nunca_expuesta(self):
        creacion = self.client.post(URL, self.datos(), format="json")
        self.assertNotIn("contrasenia", creacion.json())
        listado = self.client.get(URL)
        for perfil in listado.json():
            self.assertNotIn("contrasenia", perfil)
        detalle = self.client.get(f"{URL}{DOC}/")
        self.assertNotIn("contrasenia", detalle.json())

    def test_contrasenia_debil_rechazada(self):
        respuesta = self.client.post(URL, self.datos("123"), format="json")
        self.assertEqual(respuesta.status_code, 400, respuesta.content)
        self.assertIn("contrasenia", respuesta.json())

    def test_listar_activos(self):
        respuesta = self.client.get(f"{URL}activos/")
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        datos = respuesta.json()
        self.assertEqual(len(datos), 2)
        self.assertTrue(all(item["estado_perfil"] for item in datos))
        self.assertTrue(all("contrasenia" not in item for item in datos))


class LoginTests(APITestCaseBase):
    URL_LOGIN = "/api/usuarios/login/"

    def test_login_devuelve_tokens_y_datos(self):
        respuesta = self.client.post(
            self.URL_LOGIN,
            {"num_documento": "1000000001", "contrasenia": "hash-prueba-1"},
            format="json",
        )
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        datos = respuesta.json()
        self.assertIn("access", datos)
        self.assertIn("refresh", datos)
        self.assertEqual(datos["num_documento"], "1000000001")
        self.assertEqual(datos["nombre_completo"], "Ana Lopez Gomez")
        self.assertEqual(datos["rol"], "Administrador")

    def test_login_credenciales_invalidas(self):
        respuesta = self.client.post(
            self.URL_LOGIN,
            {"num_documento": "1000000001", "contrasenia": "incorrecta"},
            format="json",
        )
        self.assertEqual(respuesta.status_code, 401, respuesta.content)

    def test_login_perfil_inactivo(self):
        respuesta = self.client.post(
            self.URL_LOGIN,
            {"num_documento": "1000000003", "contrasenia": "hash-prueba-3"},
            format="json",
        )
        self.assertEqual(respuesta.status_code, 403, respuesta.content)

    def test_token_de_login_resuelve_el_perfil(self):
        respuesta = self.client.post(
            self.URL_LOGIN,
            {"num_documento": "1000000001", "contrasenia": "hash-prueba-1"},
            format="json",
        )
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        token = AccessToken(respuesta.json()["access"])
        perfil = PerfilJWTAuthentication().get_user(token)
        self.assertEqual(perfil.pk, "1000000001")
        self.assertTrue(perfil.is_authenticated)
        self.assertFalse(perfil.is_anonymous)
