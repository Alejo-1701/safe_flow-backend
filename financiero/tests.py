from decimal import Decimal

from accesos.models import Turno
from config.test_helpers import (
    ApiTestCaseBase,
    crear_pago,
    crear_registro,
    crear_tarifa,
    crear_turno,
)

from .models import Pago


class FinancieroApiTests(ApiTestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.turno = crear_turno()

    def test_delete_pago_rechazado(self):
        response = self.client.delete("/api/financiero/pagos/")
        self.assertEqual(response.status_code, 405)

    def test_delete_recaudo_rechazado(self):
        response = self.client.delete("/api/financiero/recaudos/")
        self.assertEqual(response.status_code, 405)

    def test_tarifa_mantiene_delete_disponible(self):
        tarifa = crear_tarifa()
        response = self.client.delete(f"/api/financiero/tarifas/{tarifa.id_tarifa}/")
        self.assertEqual(response.status_code, 204)

    def test_arqueo_turno_cuadrado(self):
        crear_pago("12000.00", id_turno=self.turno)
        crear_pago("3000.00", id_turno=self.turno)

        response = self.client.post(
            "/api/financiero/pagos/arqueo-turno/",
            {
                "id_turno": self.turno.id_turno,
                "recaudo_fisico": "15000.00",
                "observaciones": "Arqueo sin novedades",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_sistema"], "15000.00")
        self.assertEqual(response.data["diferencia"], "0.00")
        self.assertEqual(response.data["estado"], "Cuadrado")

        self.turno.refresh_from_db()
        self.assertEqual(self.turno.recaudo_fisico, Decimal("15000.00"))
        self.assertEqual(self.turno.observaciones, "Arqueo sin novedades")
        self.assertEqual(self.turno.estado, "Cuadrado")

    def test_arqueo_turno_descuadre(self):
        crear_pago("15000.00", id_turno=self.turno)

        response = self.client.post(
            "/api/financiero/pagos/arqueo-turno/",
            {
                "id_turno": self.turno.id_turno,
                "recaudo_fisico": "14500.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["diferencia"], "-500.00")
        self.assertEqual(response.data["estado"], "Descuadre detectado")

        self.turno.refresh_from_db()
        self.assertEqual(self.turno.estado, "Descuadre detectado")

    def test_arqueo_turno_inexistente(self):
        response = self.client.post(
            "/api/financiero/pagos/arqueo-turno/",
            {"id_turno": 999999, "recaudo_fisico": "100.00"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_pago_puede_crearse_y_listarse(self):
        registro = crear_registro(id_turno=self.turno)
        response = self.client.post(
            "/api/financiero/pagos/",
            {
                "metodo_pago": "Efectivo",
                "fecha_caja": "2026-11-26",
                "hora_caja": "12:00:00",
                "monto_total": "7500.00",
                "id_registro": registro.id_registro,
                "id_turno": self.turno.id_turno,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Pago.objects.count(), 1)
        self.assertEqual(Turno.objects.count(), 1)
