from config.test_helpers import APITestCaseBase
from novedades.models import Solicitud

INCIDENTES = "/api/novedades/incidentes/"
SOLICITUDES = "/api/novedades/solicitudes/"


class NovedadesAPITests(APITestCaseBase):
    def test_rutas_responden_get(self):
        for ruta in (INCIDENTES, SOLICITUDES):
            self.comprobar_get(ruta)

    def test_datos_semilla_disponibles(self):
        for ruta, campo in (
            (INCIDENTES, "id_incidente"),
            (SOLICITUDES, "id_solicitud"),
        ):
            with self.subTest(ruta=ruta):
                respuesta = self.client.get(ruta)
                self.assertEqual(respuesta.status_code, 200)
                self.assertEqual(len(respuesta.json()), 1)
                self.assertIn(campo, respuesta.json()[0])

    def test_crear_incidente(self):
        respuesta = self.client.post(
            INCIDENTES,
            {
                "doc_persona": "1000000003",
                "descripcion": "Porton con falla intermitente",
                "fecha_incidente": "2026-11-24",
            },
            format="json",
        )
        self.assertEqual(respuesta.status_code, 201, respuesta.content)
        self.comprobar_get(f"{INCIDENTES}{respuesta.json()['id_incidente']}/")

    def test_crear_y_actualizar_solicitud(self):
        respuesta = self.client.post(
            SOLICITUDES,
            {
                "doc_persona": "1000000003",
                "descripcion": "Reposicion de llavero",
                "fecha_solicitud": "2026-11-24",
            },
            format="json",
        )
        self.assertEqual(respuesta.status_code, 201, respuesta.content)
        id_solicitud = respuesta.json()["id_solicitud"]
        self.assertEqual(respuesta.json()["estado_solicitud"], "Pendiente")

        detalle = f"{SOLICITUDES}{id_solicitud}/"
        self.comprobar_get(detalle)
        respuesta = self.client.patch(
            detalle,
            {"estado_solicitud": "Rechazada"},
            format="json",
        )
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        self.assertEqual(respuesta.json()["estado_solicitud"], "Rechazada")

    def test_cambiar_estado_de_solicitud(self):
        respuesta = self.client.patch(
            f"{SOLICITUDES}1/cambiar-estado/",
            {"estado_solicitud": "Aprobada"},
            format="json",
        )
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        self.assertEqual(respuesta.json()["estado_solicitud"], "Aprobada")
        self.assertEqual(Solicitud.objects.get(pk=1).estado_solicitud, "Aprobada")
