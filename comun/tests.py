from config.test_helpers import APITestCaseBase


class NotificacionCRUDTests(APITestCaseBase):
    def test_ciclo_completo(self):
        self.ciclo_crud(
            {
                "url": "/api/comun/notificaciones/",
                "pk": "id_notificacion",
                "crear": lambda: {
                    "tipo": "Prueba",
                    "mensaje": "Mensaje de prueba",
                    "leido": False,
                    "numero_documento": "1000000003",
                },
                "actualizar": lambda pk: {
                    "tipo": "Actualizada",
                    "mensaje": "Mensaje actualizado",
                    "leido": True,
                    "numero_documento": "1000000003",
                },
                "parchear": {"leido": False},
            }
        )


class NotificacionEstadoCRUDTests(APITestCaseBase):
    def test_ciclo_completo(self):
        self.ciclo_crud(
            {
                "url": "/api/comun/notificacion-estados/",
                "pk": "id_estado_hist",
                "crear": lambda: {
                    "notificacion": 1,
                    "nuevo_estado": "Revision",
                    "duracion": "01:00:00",
                    "fecha_cambio": "2026-11-25",
                    "hora_cambio": "09:00:00",
                },
                "actualizar": lambda pk: {
                    "notificacion": 1,
                    "nuevo_estado": "Proceso",
                    "duracion": "02:00:00",
                    "fecha_cambio": "2026-11-25",
                    "hora_cambio": "10:00:00",
                },
                "parchear": {"nuevo_estado": "Resuelto"},
            }
        )
