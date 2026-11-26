from decimal import Decimal

from accesos.models import Turno
from config.test_helpers import APITestCaseBase

TARIFAS = "/api/financiero/tarifas/"
PAGOS = "/api/financiero/pagos/"
RECAUDOS = "/api/financiero/recaudos/"
REGISTROS = "/api/accesos/registros-acceso/"


class FinancieroAPITests(APITestCaseBase):
    def test_rutas_responden_get(self):
        for ruta in (TARIFAS, PAGOS, RECAUDOS):
            self.comprobar_get(ruta)

    def test_datos_semilla_disponibles(self):
        for ruta, campo in (
            (TARIFAS, "id_tarifa"),
            (PAGOS, "id_pago"),
            (RECAUDOS, "numero_factura"),
        ):
            with self.subTest(ruta=ruta):
                respuesta = self.client.get(ruta)
                self.assertEqual(respuesta.status_code, 200)
                self.assertEqual(len(respuesta.json()), 1)
                self.assertIn(campo, respuesta.json()[0])

    def test_ciclo_crud_de_tarifas(self):
        self.ciclo_crud(
            {
                "url": TARIFAS,
                "pk": "id_tarifa",
                "crear": lambda: {
                    "tipo_vehiculo": "Moto",
                    "valor_minuto": "900.00",
                    "id_asamblea": 1,
                },
                "actualizar": lambda pk: {
                    "tipo_vehiculo": "Moto",
                    "valor_minuto": "950.00",
                    "id_asamblea": 1,
                },
                "parchear": {"valor_minuto": "1000.00"},
            }
        )

    def test_crear_pago_y_recaudo(self):
        respuesta = self.client.post(
            REGISTROS,
            {
                "placa": "ABC123",
                "id_turno": 1,
                "fecha_entrada": "2026-11-24",
                "hora_entrada": "18:00:00",
            },
            format="json",
        )
        self.assertEqual(respuesta.status_code, 201, respuesta.content)
        id_registro = respuesta.json()["id_registro"]

        respuesta = self.client.post(
            PAGOS,
            {
                "metodo_pago": "Tarjeta",
                "fecha_caja": "2026-11-24",
                "hora_caja": "18:10:00",
                "monto_total": "5000.00",
                "id_registro": id_registro,
                "id_turno": 1,
            },
            format="json",
        )
        self.assertEqual(respuesta.status_code, 201, respuesta.content)
        id_pago = respuesta.json()["id_pago"]
        self.comprobar_get(f"{PAGOS}{id_pago}/")

        respuesta = self.client.post(
            RECAUDOS,
            {
                "id_pago": id_pago,
                "id_tarifa": 1,
                "id_confirmacion": "CONF-0002",
                "sub_total": "5000.00",
                "total_pagado": "5000.00",
            },
            format="json",
        )
        self.assertEqual(respuesta.status_code, 201, respuesta.content)
        numero_factura = respuesta.json()["numero_factura"]
        self.assertEqual(Decimal(respuesta.json()["total_pagado"]), Decimal("5000.00"))
        self.comprobar_get(f"{RECAUDOS}{numero_factura}/")

    def test_arqueo_turno_cuadrado(self):
        respuesta = self.client.post(
            f"{PAGOS}arqueo-turno/",
            {"id_turno": 1, "recaudo_fisico": "10200.00"},
            format="json",
        )
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        datos = respuesta.json()
        self.assertEqual(Decimal(datos["total_sistema"]), Decimal("10200.00"))
        self.assertEqual(Decimal(datos["diferencia"]), Decimal("0.00"))
        self.assertEqual(datos["estado"], "Cuadrado")
        self.assertEqual(Turno.objects.get(pk=1).estado, "Cuadrado")
