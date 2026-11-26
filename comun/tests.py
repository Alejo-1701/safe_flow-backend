from datetime import datetime

from django.utils import timezone

from config.test_helpers import ApiTestCaseBase, crear_notificacion

from .models import Notificacion


class NotificacionesApiTests(ApiTestCaseBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.vieja = crear_notificacion(tipo="Aviso", mensaje="Notificación antigua")
        cls.nueva = crear_notificacion(tipo="Alerta", mensaje="Notificación reciente")

        Notificacion.objects.filter(pk=cls.vieja.pk).update(
            fecha_creacion=timezone.make_aware(datetime(2026, 1, 1, 8, 0))
        )
        Notificacion.objects.filter(pk=cls.nueva.pk).update(
            fecha_creacion=timezone.make_aware(datetime(2026, 11, 26, 8, 0))
        )

    def test_filtro_por_numero_documento_ordena_mas_reciente_primero(self):
        response = self.client.get(
            "/api/comun/notificaciones/?numero_documento=10000001"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["id_notificacion"], self.nueva.id_notificacion)
        self.assertEqual(response.data[1]["id_notificacion"], self.vieja.id_notificacion)
        self.assertIn("fecha_creacion", response.data[0])

    def test_listado_sin_parametro_devuelve_todas(self):
        response = self.client.get("/api/comun/notificaciones/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_filtro_sin_coincidencias_devuelve_vacio(self):
        response = self.client.get(
            "/api/comun/notificaciones/?numero_documento=99999999"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
