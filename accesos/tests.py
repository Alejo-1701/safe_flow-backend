from config.test_helpers import (
    ApiTestCaseBase,
    crear_celda,
    crear_persona,
    crear_registro,
    crear_turno,
    crear_vehiculo,
)

from .models import RegistroAcceso


class AccesosApiTests(ApiTestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.persona = crear_persona()
        cls.vehiculo = crear_vehiculo()
        cls.turno = crear_turno()

    def test_ingreso_asigna_celda_disponible(self):
        celda = crear_celda()

        response = self.client.post(
            "/api/accesos/registros-acceso/ingreso/",
            {"placa": "ABC123", "id_turno": self.turno.id_turno},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["celda_asignada"], "P-01")

        celda.refresh_from_db()
        self.assertEqual(celda.estado, "Ocupado")

        registro = RegistroAcceso.objects.get(pk=response.data["id_registro"])
        self.assertEqual(registro.celda_asignada_id, "P-01")

    def test_ingreso_con_vehiculo_inexistente_devuelve_400(self):
        crear_celda()
        response = self.client.post(
            "/api/accesos/registros-acceso/ingreso/",
            {"placa": "ZZZ999", "id_turno": self.turno.id_turno},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_ingreso_sin_cupo_devuelve_400(self):
        response = self.client.post(
            "/api/accesos/registros-acceso/ingreso/",
            {"placa": "ABC123", "id_turno": self.turno.id_turno},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_turno_rechazado(self):
        response = self.client.delete(f"/api/accesos/turnos/{self.turno.id_turno}/")
        self.assertEqual(response.status_code, 405)

    def test_delete_registro_rechazado(self):
        registro = crear_registro(id_turno=self.turno)
        response = self.client.delete(
            f"/api/accesos/registros-acceso/{registro.id_registro}/"
        )
        self.assertEqual(response.status_code, 405)
