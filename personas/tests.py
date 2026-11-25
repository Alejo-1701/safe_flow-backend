from config.test_helpers import APITestCaseBase
from personas.models import Persona, PersonaCorreo, PersonaTelefono

DOC = "TST002"
DOC_NUEVA = "TST003"
NIT = "900999001"


class PersonasCRUDTests(APITestCaseBase):
    def setUp(self):
        Persona.objects.create(
            num_documento=DOC,
            tipo_documento="CC",
            primer_nombre="Soporte",
            primer_apellido="Prueba",
            segundo_apellido="Test",
            id_rol_id=1,
            nit_empresa_id="900123456",
        )

    def test_crud_en_los_ocho_recursos(self):
        casos = [
            {
                "nombre": "roles",
                "url": "/api/personas/roles/",
                "pk": "id_rol",
                "crear": lambda: {"nombre_rol": "RolNuevo"},
                "actualizar": lambda pk: {"nombre_rol": "RolActualizado"},
                "parchear": {"nombre_rol": "RolParcheado"},
            },
            {
                "nombre": "empresas",
                "url": "/api/personas/empresas/",
                "pk": "nit",
                "crear": lambda: {
                    "nit": NIT,
                    "nombre_empresa": "Empresa Nueva",
                    "rep_legal": "Representante",
                    "telefono": "3001234567",
                    "email": "empresa@test.com",
                    "direccion": "Calle 1 #2-3",
                },
                "actualizar": lambda pk: {
                    "nit": NIT,
                    "nombre_empresa": "Empresa Actualizada",
                    "rep_legal": "Representante",
                    "telefono": "3001234567",
                    "email": "empresa@test.com",
                    "direccion": "Calle 1 #2-3",
                },
                "parchear": {"nombre_empresa": "Empresa Parcheada"},
            },
            {
                "nombre": "personas",
                "url": "/api/personas/personas/",
                "pk": "num_documento",
                "crear": lambda: {
                    "num_documento": DOC_NUEVA,
                    "tipo_documento": "TI",
                    "primer_nombre": "Nueva",
                    "segundo_nombre": None,
                    "primer_apellido": "Persona",
                    "segundo_apellido": "Prueba",
                    "id_rol": 1,
                    "nit_empresa": "900123456",
                },
                "actualizar": lambda pk: {
                    "num_documento": DOC_NUEVA,
                    "tipo_documento": "TI",
                    "primer_nombre": "Actualizada",
                    "segundo_nombre": None,
                    "primer_apellido": "Persona",
                    "segundo_apellido": "Prueba",
                    "id_rol": 1,
                    "nit_empresa": "900123456",
                },
                "parchear": {"primer_nombre": "Parcheada"},
            },
            {
                "nombre": "telefonos",
                "url": "/api/personas/telefonos/",
                "pk": "doc_persona",
                "crear": lambda: {"doc_persona": DOC, "telefono": "3000000001"},
                "actualizar": lambda pk: {"doc_persona": pk, "telefono": "3000000002"},
                "parchear": {"telefono": "3000000003"},
            },
            {
                "nombre": "correos",
                "url": "/api/personas/correos/",
                "pk": "doc_persona",
                "crear": lambda: {"doc_persona": DOC, "email": "nuevo@test.com"},
                "actualizar": lambda pk: {"doc_persona": pk, "email": "actualizado@test.com"},
                "parchear": {"email": "parcheado@test.com"},
            },
            {
                "nombre": "administradores",
                "url": "/api/personas/administradores/",
                "pk": "numero_documento",
                "crear": lambda: {
                    "numero_documento": DOC,
                    "rol": "Admin prueba",
                    "inicio_gestion": "2026-01-01",
                    "fin_gestion": None,
                },
                "actualizar": lambda pk: {
                    "numero_documento": pk,
                    "rol": "Admin actualizado",
                    "inicio_gestion": "2026-02-01",
                    "fin_gestion": None,
                },
                "parchear": {"rol": "Admin parcheado"},
            },
            {
                "nombre": "guardias",
                "url": "/api/personas/guardias/",
                "pk": "numero_documento",
                "crear": lambda: {"numero_documento": DOC, "empresa": "Empresa prueba"},
                "actualizar": lambda pk: {"numero_documento": pk, "empresa": "Empresa actualizada"},
                "parchear": {"empresa": "Empresa parcheada"},
            },
            {
                "nombre": "residentes",
                "url": "/api/personas/residentes/",
                "pk": "numero_documento",
                "crear": lambda: {"numero_documento": DOC, "id_apartamento": 402},
                "actualizar": lambda pk: {"numero_documento": pk, "id_apartamento": 402},
                "parchear": {"id_apartamento": 402},
            },
        ]
        for caso in casos:
            with self.subTest(recurso=caso["nombre"]):
                self.ciclo_crud(caso)


class PersonasValidacionesTests(APITestCaseBase):
    def test_foreign_keys_como_cadena_se_resuelven(self):
        respuesta = self.client.post(
            "/api/personas/personas/",
            {
                "num_documento": DOC_NUEVA,
                "tipo_documento": "TI",
                "primer_nombre": "Nueva",
                "primer_apellido": "Persona",
                "segundo_apellido": "Prueba",
                "id_rol": "1",
                "nit_empresa": "900123456",
            },
            format="json",
        )
        self.assertEqual(respuesta.status_code, 201, respuesta.content)
        self.assertEqual(Persona.objects.get(num_documento=DOC_NUEVA).id_rol_id, 1)

    def test_foreign_key_inexistente_devuelve_400(self):
        respuesta = self.client.post(
            "/api/personas/personas/",
            {
                "num_documento": DOC_NUEVA,
                "tipo_documento": "TI",
                "primer_nombre": "Nueva",
                "primer_apellido": "Persona",
                "segundo_apellido": "Prueba",
                "id_rol": 999999,
                "nit_empresa": "900123456",
            },
            format="json",
        )
        self.assertEqual(respuesta.status_code, 400, respuesta.content)

    def test_eliminar_con_dependencias_devuelve_409(self):
        respuesta = self.client.delete("/api/personas/personas/1000000001/")
        self.assertEqual(respuesta.status_code, 409, respuesta.content)


class PersonasAccionesTests(APITestCaseBase):
    def test_listar_por_rol(self):
        respuesta = self.client.get("/api/personas/personas/por-rol/1/")
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        self.assertEqual([item["num_documento"] for item in respuesta.json()], ["1000000001"])

    def test_listar_por_empresa(self):
        respuesta = self.client.get("/api/personas/personas/por-empresa/900123456/")
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        self.assertEqual(len(respuesta.json()), 2)

    def test_listar_telefonos_por_persona(self):
        respuesta = self.client.get("/api/personas/telefonos/por-persona/1000000001/")
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        self.assertEqual(len(respuesta.json()), 1)

    def test_listar_correos_por_persona(self):
        respuesta = self.client.get("/api/personas/correos/por-persona/1000000001/")
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        self.assertEqual(len(respuesta.json()), 1)

    def test_detalle_de_telefono_se_desambigua(self):
        PersonaTelefono.objects.create(doc_persona_id="1000000001", telefono="3009998877")
        respuesta = self.client.get("/api/personas/telefonos/1000000001/?telefono=3009998877")
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        self.assertEqual(respuesta.json()["telefono"], "3009998877")

    def test_detalle_de_correo_se_desambigua(self):
        PersonaCorreo.objects.create(doc_persona_id="1000000001", email="ana.segunda@example.com")
        respuesta = self.client.get("/api/personas/correos/1000000001/?email=ana.segunda@example.com")
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        self.assertEqual(respuesta.json()["email"], "ana.segunda@example.com")
