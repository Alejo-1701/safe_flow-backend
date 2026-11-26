from rest_framework.test import APITestCase

RUTAS_SOLO_LECTURA = (
    "/api/vehiculos/",
    "/api/infraestructura/apartamentos/",
    "/api/infraestructura/parqueaderos/",
    "/api/infraestructura/asambleas/",
    "/api/accesos/turnos/",
    "/api/accesos/registros-acceso/",
    "/api/visitas/autorizaciones/",
    "/api/financiero/tarifas/",
    "/api/financiero/pagos/",
    "/api/financiero/recaudos/",
    "/api/novedades/incidentes/",
    "/api/novedades/solicitudes/",
)

RUTAS_CRUD = (
    "/api/comun/notificaciones/",
    "/api/comun/notificacion-estados/",
    "/api/usuarios/perfiles/",
    "/api/personas/roles/",
    "/api/personas/empresas/",
    "/api/personas/personas/",
    "/api/personas/telefonos/",
    "/api/personas/correos/",
    "/api/personas/administradores/",
    "/api/personas/guardias/",
    "/api/personas/residentes/",
)


class APITestCaseBase(APITestCase):
    def comprobar_solo_lectura(self, ruta):
        respuesta = self.client.get(ruta)
        self.assertEqual(respuesta.status_code, 200, respuesta.content)
        for metodo in ("post", "put", "patch", "delete"):
            with self.subTest(metodo=metodo, ruta=ruta):
                respuesta = getattr(self.client, metodo)(ruta, data={}, format="json")
                self.assertEqual(respuesta.status_code, 405, respuesta.content)

    def ciclo_crud(self, caso):
        url = caso["url"]
        respuesta = self.client.post(url, caso["crear"](), format="json")
        self.assertEqual(respuesta.status_code, 201, respuesta.content)
        pk = respuesta.json()[caso["pk"]]
        detalle = f"{url}{pk}/"

        respuesta = self.client.get(detalle)
        self.assertEqual(respuesta.status_code, 200, respuesta.content)

        respuesta = self.client.put(detalle, caso["actualizar"](pk), format="json")
        self.assertEqual(respuesta.status_code, 200, respuesta.content)

        respuesta = self.client.patch(detalle, caso["parchear"], format="json")
        self.assertEqual(respuesta.status_code, 200, respuesta.content)

        respuesta = self.client.delete(detalle)
        self.assertEqual(respuesta.status_code, 204, respuesta.content)
