from config.test_helpers import ApiTestCaseBase, crear_asamblea


class AsambleaApiTests(ApiTestCaseBase):
    def test_asamblea_acepta_post_put_patch_y_rechaza_delete(self):
        response = self.client.post(
            "/api/infraestructura/asambleas/",
            {
                "numero_acta": "ACT-002",
                "fecha_reunion": "2026-11-20",
                "art_referencia": "Art. 8",
                "des_acuerdo": "Acuerdo de prueba",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        id_asamblea = response.data["id_asamblea"]

        response = self.client.put(
            f"/api/infraestructura/asambleas/{id_asamblea}/",
            {
                "numero_acta": "ACT-002",
                "fecha_reunion": "2026-11-20",
                "art_referencia": "Art. 9",
                "des_acuerdo": "Acuerdo actualizado",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.patch(
            f"/api/infraestructura/asambleas/{id_asamblea}/",
            {"des_acuerdo": "Acuerdo parcheado"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(
            f"/api/infraestructura/asambleas/{id_asamblea}/"
        )
        self.assertEqual(response.status_code, 405)

    def test_asamblea_existente_se_listaba(self):
        crear_asamblea()
        response = self.client.get("/api/infraestructura/asambleas/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
