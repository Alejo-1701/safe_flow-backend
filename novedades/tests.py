from config.test_helpers import ApiTestCaseBase, crear_solicitud


class NovedadesApiTests(ApiTestCaseBase):
    def test_delete_incidente_rechazado(self):
        response = self.client.delete("/api/novedades/incidentes/")
        self.assertEqual(response.status_code, 405)

    def test_delete_solicitud_rechazado(self):
        response = self.client.delete("/api/novedades/solicitudes/")
        self.assertEqual(response.status_code, 405)

    def test_cambiar_estado_solicitud(self):
        solicitud = crear_solicitud()

        response = self.client.patch(
            f"/api/novedades/solicitudes/{solicitud.id_solicitud}/cambiar-estado/",
            {"estado_solicitud": "Aprobada"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["estado_solicitud"], "Aprobada")

        solicitud.refresh_from_db()
        self.assertEqual(solicitud.estado_solicitud, "Aprobada")

    def test_cambiar_estado_rechaza_valor_invalido(self):
        solicitud = crear_solicitud(num_documento="10000002")

        response = self.client.patch(
            f"/api/novedades/solicitudes/{solicitud.id_solicitud}/cambiar-estado/",
            {"estado_solicitud": "NoValido"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        solicitud.refresh_from_db()
        self.assertEqual(solicitud.estado_solicitud, "Pendiente")

    def test_patch_normal_de_solicitud_seguia_permitido(self):
        solicitud = crear_solicitud(num_documento="10000003")
        response = self.client.patch(
            f"/api/novedades/solicitudes/{solicitud.id_solicitud}/",
            {"descripcion": "Descripción actualizada"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
