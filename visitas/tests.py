from config.test_helpers import ApiTestCaseBase, crear_persona


class AutorizacionVisitaApiTests(ApiTestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        crear_persona("10000001")
        crear_persona("10000002")

    def test_autorizacion_acepta_crud_completo(self):
        response = self.client.post(
            "/api/visitas/autorizaciones/",
            {
                "fecha_programada": "2026-11-27",
                "doc_residente": "10000001",
                "doc_visitante": "10000002",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        id_autorizacion = response.data["id_autorizacion"]

        response = self.client.delete(
            f"/api/visitas/autorizaciones/{id_autorizacion}/"
        )
        self.assertEqual(response.status_code, 204)
