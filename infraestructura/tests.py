from config.test_helpers import APITestCaseBase


class InfraestructuraSoloLecturaTests(APITestCaseBase):
    def test_solo_lectura(self):
        for ruta in (
            "/api/infraestructura/apartamentos/",
            "/api/infraestructura/parqueaderos/",
            "/api/infraestructura/asambleas/",
        ):
            self.comprobar_solo_lectura(ruta)

    def test_filtro_de_apartamentos_por_torre(self):
        respuesta = self.client.get("/api/infraestructura/apartamentos/", {"torre": "A"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 1)

    def test_filtro_de_parqueaderos_por_estado(self):
        respuesta = self.client.get("/api/infraestructura/parqueaderos/", {"estado": "Disponible"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual([item["id_parqueadero"] for item in respuesta.json()], ["P-001"])
