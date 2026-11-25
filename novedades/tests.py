from config.test_helpers import APITestCaseBase


class NovedadesSoloLecturaTests(APITestCaseBase):
    def test_solo_lectura(self):
        for ruta in ("/api/novedades/incidentes/", "/api/novedades/solicitudes/"):
            self.comprobar_solo_lectura(ruta)

    def test_datos_semilla_disponibles(self):
        for ruta, campo in (
            ("/api/novedades/incidentes/", "id_incidente"),
            ("/api/novedades/solicitudes/", "id_solicitud"),
        ):
            with self.subTest(ruta=ruta):
                respuesta = self.client.get(ruta)
                self.assertEqual(respuesta.status_code, 200)
                self.assertEqual(len(respuesta.json()), 1)
                self.assertIn(campo, respuesta.json()[0])
