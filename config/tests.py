import inspect

from django.apps import apps
from django.db import models
from django.test import SimpleTestCase
from rest_framework import serializers

from accesos import serializers as accesos_serializers
from comun import serializers as comun_serializers
from config.test_helpers import APITestCaseBase, RUTAS_CRUD, RUTAS_SOLO_LECTURA
from financiero import serializers as financiero_serializers
from infraestructura import serializers as infraestructura_serializers
from novedades import serializers as novedades_serializers
from personas import serializers as personas_serializers
from usuarios import serializers as usuarios_serializers
from vehiculos import serializers as vehiculos_serializers
from visitas import serializers as visitas_serializers

APPS = (
    "accesos",
    "comun",
    "financiero",
    "infraestructura",
    "novedades",
    "personas",
    "usuarios",
    "vehiculos",
    "visitas",
)

TABLAS = {
    "administrador",
    "apartamento",
    "asamblea_copropietarios",
    "autorizacion_visita",
    "empresa_vigilancia",
    "guardia_seguridad",
    "incidentes",
    "notificacion",
    "notificacion_estados",
    "pago",
    "parqueadero",
    "perfil",
    "persona_correo",
    "persona_telefonos",
    "personas",
    "recaudo",
    "registro_acceso",
    "residente",
    "roles",
    "solicitud",
    "tarifa",
    "turno",
    "vehiculos",
}

MODULOS_SERIALIZERS = (
    accesos_serializers,
    comun_serializers,
    financiero_serializers,
    infraestructura_serializers,
    novedades_serializers,
    personas_serializers,
    usuarios_serializers,
    vehiculos_serializers,
    visitas_serializers,
)


class SuperficieAPITests(APITestCaseBase):
    def test_las_23_rutas_responden_get(self):
        for ruta in RUTAS_CRUD + RUTAS_SOLO_LECTURA:
            with self.subTest(ruta=ruta):
                respuesta = self.client.get(ruta)
                self.assertEqual(respuesta.status_code, 200, respuesta.content)

    def test_escritura_solo_en_apps_core(self):
        self.assertEqual(len(RUTAS_CRUD), 11)
        self.assertEqual(len(RUTAS_SOLO_LECTURA), 12)
        for ruta in RUTAS_SOLO_LECTURA:
            self.comprobar_solo_lectura(ruta)

    def test_detalle_inexistente_devuelve_404(self):
        respuesta = self.client.get("/api/accesos/turnos/9999999999/")
        self.assertEqual(respuesta.status_code, 404)

    def test_contrasenia_no_aparece_en_listado_de_perfiles(self):
        respuesta = self.client.get("/api/usuarios/perfiles/")
        self.assertEqual(respuesta.status_code, 200)
        for perfil in respuesta.json():
            self.assertNotIn("contrasenia", perfil)


class ContratoModelosTests(SimpleTestCase):
    def test_tablas_y_relaciones(self):
        tablas = set()
        for etiqueta in APPS:
            for modelo in apps.get_app_config(etiqueta).get_models():
                self.assertFalse(modelo._meta.managed, modelo._meta.label)
                self.assertTrue(modelo._meta.db_table, modelo._meta.label)
                tablas.add(modelo._meta.db_table)
                for campo in modelo._meta.fields:
                    if campo.many_to_one:
                        self.assertEqual(
                            campo.remote_field.on_delete,
                            models.DO_NOTHING,
                            f"{modelo._meta.label}.{campo.name}",
                        )
        self.assertEqual(tablas, TABLAS)


class ContratoSerializersTests(SimpleTestCase):
    def test_campos_explicitos(self):
        encontrados = 0
        for modulo in MODULOS_SERIALIZERS:
            for _, clase in inspect.getmembers(modulo, inspect.isclass):
                if not issubclass(clase, serializers.ModelSerializer):
                    continue
                if "Meta" not in clase.__dict__:
                    continue
                encontrados += 1
                self.assertNotEqual(clase.Meta.fields, "__all__", clase.__name__)
        self.assertEqual(encontrados, 23)
