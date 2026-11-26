from config.test_helpers import APITestCaseBase


class AccesosSoloLecturaTests(APITestCaseBase):
    def test_solo_lectura(self):
        for ruta in ("/api/accesos/turnos/", "/api/accesos/registros-acceso/"):
            self.comprobar_solo_lectura(ruta)

    def test_filtro_de_turnos_por_guardia(self):
        respuesta = self.client.get("/api/accesos/turnos/", {"num_documento_guardia": "1000000002"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 1)

    def test_filtro_de_registros_por_placa(self):
        respuesta = self.client.get("/api/accesos/registros-acceso/", {"placa": "abc123"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 1)
