from config.test_helpers import APITestCaseBase

APARTAMENTOS = "/api/infraestructura/apartamentos/"
PARQUEADEROS = "/api/infraestructura/parqueaderos/"
ASAMBLEAS = "/api/infraestructura/asambleas/"


class InfraestructuraAPITests(APITestCaseBase):
    def test_solo_lectura_de_apartamentos_y_parqueaderos(self):
        for ruta in (APARTAMENTOS, PARQUEADEROS):
            self.comprobar_solo_lectura(ruta)

    def test_asambleas_responden_get(self):
        self.comprobar_get(ASAMBLEAS)

    def test_filtro_de_apartamentos_por_torre(self):
        respuesta = self.client.get(APARTAMENTOS, {"torre": "A"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 1)

    def test_filtro_de_parqueaderos_por_estado(self):
        respuesta = self.client.get(PARQUEADEROS, {"estado": "Disponible"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual([item["id_parqueadero"] for item in respuesta.json()], ["P-001"])

    def test_crear_actualizar_asamblea(self):
        respuesta = self.client.post(
            ASAMBLEAS,
            {
                "numero_acta": "ACT-002",
                "fecha_reunion": "2026-11-20",
                "art_referencia": "Articulo 15",
                "des_acuerdo": "Se aprueba el presupuesto",
            },
            format="json",
        )
        self.assertEqual(respuesta.status_code, 201, respuesta.content)
        id_asamblea = respuesta.json()["id_asamblea"]

        detalle = f"{ASAMBLEAS}{id_asamblea}/"
        self.comprobar_get(detalle)
        respuesta = self.client.put(
            detalle,
            {
                "numero_acta": "ACT-003",
                "fecha_reunion": "2026-11-21",
                "art_referencia": "Articulo 16",
                "des_acuerdo": "Se aprueba el cronograma",
            },
            format="json",
        )
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        self.assertEqual(respuesta.json()["numero_acta"], "ACT-003")

        respuesta = self.client.patch(
            detalle,
            {"des_acuerdo": "Se aprueba el cronograma ajustado"},
            format="json",
        )
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        self.assertEqual(respuesta.json()["des_acuerdo"], "Se aprueba el cronograma ajustado")
