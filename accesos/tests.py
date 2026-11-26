from config.test_helpers import APITestCaseBase
from infraestructura.models import Parqueadero

TURNOS = "/api/accesos/turnos/"
REGISTROS = "/api/accesos/registros-acceso/"


class AccesosAPITests(APITestCaseBase):
    def test_rutas_responden_get(self):
        for ruta in (TURNOS, REGISTROS):
            self.comprobar_get(ruta)

    def test_filtro_de_turnos_por_guardia(self):
        respuesta = self.client.get(TURNOS, {"num_documento_guardia": "1000000002"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 1)

    def test_filtro_de_registros_por_placa(self):
        respuesta = self.client.get(REGISTROS, {"placa": "abc123"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 1)

    def test_crear_y_actualizar_turno(self):
        respuesta = self.client.post(
            TURNOS,
            {
                "fecha_turno": "2026-11-25",
                "hora_inicio": "06:00:00",
                "hora_fin": "14:00:00",
                "recaudo_fisico": "0.00",
                "num_documento_guardia": "1000000002",
            },
            format="json",
        )
        self.assertEqual(respuesta.status_code, 201, respuesta.content)
        id_turno = respuesta.json()["id_turno"]
        self.assertEqual(respuesta.json()["estado"], "Abierto")

        detalle = f"{TURNOS}{id_turno}/"
        self.comprobar_get(detalle)
        respuesta = self.client.patch(detalle, {"observaciones": "Turno revisado"}, format="json")
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        self.assertEqual(respuesta.json()["observaciones"], "Turno revisado")

    def test_crear_y_actualizar_registro(self):
        respuesta = self.client.post(
            REGISTROS,
            {
                "placa": "abc123",
                "id_turno": 1,
                "fecha_entrada": "2026-11-25",
                "hora_entrada": "10:30:00",
            },
            format="json",
        )
        self.assertEqual(respuesta.status_code, 201, respuesta.content)
        id_registro = respuesta.json()["id_registro"]
        self.assertEqual(respuesta.json()["placa"], "ABC123")
        self.assertTrue(respuesta.json()["en_parqueadero"])

        detalle = f"{REGISTROS}{id_registro}/"
        self.comprobar_get(detalle)
        respuesta = self.client.patch(
            detalle,
            {"fecha_salida": "2026-11-25", "hora_salida": "12:00:00"},
            format="json",
        )
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        self.assertFalse(respuesta.json()["en_parqueadero"])

    def test_ingreso_asigna_celda_disponible(self):
        respuesta = self.client.post(
            f"{REGISTROS}ingreso/",
            {"placa": "ABC123", "id_turno": 1},
            format="json",
        )
        self.assertEqual(respuesta.status_code, 201, respuesta.content)
        datos = respuesta.json()
        self.assertEqual(datos["celda_asignada"], "P-001")
        self.assertIn("celda asignada", datos["mensaje"].lower())
        self.assertEqual(Parqueadero.objects.get(pk="P-001").estado, "Ocupado")
