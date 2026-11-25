from config.test_helpers import APITestCaseBase

URL = "/api/vehiculos/"


class VehiculoSoloLecturaTests(APITestCaseBase):
    def test_solo_lectura(self):
        self.comprobar_solo_lectura(URL)

    def test_filtro_por_propietario(self):
        respuesta = self.client.get(URL, {"doc_propietario": "1000000003"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual([item["placa"] for item in respuesta.json()], ["ABC123"])

    def test_filtro_por_tipo(self):
        respuesta = self.client.get(URL, {"tipo": "carro"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 1)
