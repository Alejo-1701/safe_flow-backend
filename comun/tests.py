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


class NotificacionAccionesTests(APITestCaseBase):
    def test_listar_no_leidas(self):
        respuesta = self.client.get("/api/comun/notificaciones/no-leidas/")
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        datos = respuesta.json()
        self.assertEqual(len(datos), 1)
        self.assertFalse(datos[0]["leido"])

    def test_listar_por_notificacion(self):
        respuesta = self.client.get("/api/comun/notificacion-estados/por-notificacion/1/")
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        datos = respuesta.json()
        self.assertEqual(len(datos), 1)
        self.assertEqual(datos[0]["notificacion"], 1)
