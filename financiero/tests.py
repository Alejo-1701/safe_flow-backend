from config.test_helpers import APITestCaseBase


class FinancieroSoloLecturaTests(APITestCaseBase):
    def test_solo_lectura(self):
        for ruta in (
            "/api/financiero/tarifas/",
            "/api/financiero/pagos/",
            "/api/financiero/recaudos/",
        ):
            self.comprobar_solo_lectura(ruta)

    def test_datos_semilla_disponibles(self):
        for ruta, campo in (
            ("/api/financiero/tarifas/", "id_tarifa"),
            ("/api/financiero/pagos/", "id_pago"),
            ("/api/financiero/recaudos/", "numero_factura"),
        ):
            with self.subTest(ruta=ruta):
                respuesta = self.client.get(ruta)
                self.assertEqual(respuesta.status_code, 200)
                self.assertEqual(len(respuesta.json()), 1)
                self.assertIn(campo, respuesta.json()[0])
