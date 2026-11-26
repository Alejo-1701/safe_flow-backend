from config.test_helpers import ApiTestCaseBase, crear_correo, crear_telefono


class PersonasContactoApiTests(ApiTestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        crear_telefono(num_documento="10000001", telefono="3001234567")
        crear_correo(num_documento="10000001", email="ana@example.com")

    def test_telefonos_se_filtran_por_doc_persona(self):
        response = self.client.get("/api/personas/telefonos/?doc_persona=10000001")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["telefono"], "3001234567")

        response = self.client.get("/api/personas/telefonos/?doc_persona=99999999")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_correos_se_filtran_por_doc_persona(self):
        response = self.client.get("/api/personas/correos/?doc_persona=10000001")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["email"], "ana@example.com")

    def test_eliminar_telefono_por_parametros(self):
        url = "/api/personas/telefonos/eliminar/?doc_persona=10000001&telefono=3001234567"

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_eliminar_correo_por_parametros(self):
        url = "/api/personas/correos/eliminar/?doc_persona=10000001&email=ana@example.com"

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_eliminar_sin_parametros_devuelve_400(self):
        response = self.client.delete("/api/personas/telefonos/eliminar/")
        self.assertEqual(response.status_code, 400)
