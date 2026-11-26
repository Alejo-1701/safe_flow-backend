from config.test_helpers import APITestCaseBase

URL = "/api/visitas/autorizaciones/"


class VisitasAPITests(APITestCaseBase):
    def test_autorizaciones_responden_get(self):
        self.comprobar_get(URL)

    def test_filtro_por_residente(self):
        respuesta = self.client.get(URL, {"doc_residente": "1000000003"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 1)

    def test_ciclo_crud_de_autorizaciones(self):
        self.ciclo_crud(
            {
                "url": URL,
                "pk": "id_autorizacion",
                "crear": lambda: {
                    "fecha_programada": "2026-11-27",
                    "doc_residente": "1000000003",
                    "doc_visitante": "1000000001",
                    "placa_vehiculo": "abc123",
                },
                "actualizar": lambda pk: {
                    "fecha_programada": "2026-11-28",
                    "doc_residente": "1000000003",
                    "doc_visitante": "1000000001",
                    "placa_vehiculo": "ABC123",
                },
                "parchear": {"fecha_programada": "2026-11-29"},
            }
        )
