from config.test_helpers import APITestCaseBase

URL = "/api/visitas/autorizaciones/"


class VisitasSoloLecturaTests(APITestCaseBase):
    def test_solo_lectura(self):
        self.comprobar_solo_lectura(URL)

    def test_filtro_por_residente(self):
        respuesta = self.client.get(URL, {"doc_residente": "1000000003"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 1)
