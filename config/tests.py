import inspect

from django.apps import apps
from django.db import connection, models
from django.test import SimpleTestCase
from django.urls import NoReverseMatch, reverse
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

from accesos.models import RegistroAcceso, Turno
from comun.models import Notificacion
from financiero.models import Pago, Recaudo, Tarifa
from infraestructura.models import Parqueadero
from personas.models import Persona

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

NOMBRES_API_ROOT = (
    "accesos-api-root",
    "comun-api-root",
    "financiero-api-root",
    "infraestructura-api-root",
    "novedades-api-root",
    "personas-api-root",
    "usuarios-api-root",
    "vehiculos-api-root",
    "visitas-api-root",
)


class SuperficieAPITests(APITestCaseBase):
    def test_admin_no_esta_disponible(self):
        respuesta = self.client.get("/admin/")
        self.assertEqual(respuesta.status_code, 404)

    def test_las_23_rutas_responden_get(self):
        for ruta in RUTAS_CRUD + RUTAS_SOLO_LECTURA:
            with self.subTest(ruta=ruta):
                respuesta = self.client.get(ruta)
                self.assertEqual(respuesta.status_code, 200, respuesta.content)

    def test_escritura_en_rutas_declaradas(self):
        self.assertEqual(len(RUTAS_CRUD), 11)
        self.assertEqual(len(RUTAS_SOLO_LECTURA), 3)
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


class AlineacionNeonTests(SimpleTestCase):
    def test_restricciones_unicas(self):
        self.assertTrue(Pago._meta.get_field("id_registro").unique)
        self.assertTrue(Recaudo._meta.get_field("id_pago").unique)
        self.assertTrue(Recaudo._meta.get_field("id_confirmacion").unique)

    def test_tipos_de_columna(self):
        self.assertEqual(Tarifa._meta.get_field("valor_minuto").max_digits, 10)
        self.assertEqual(Persona._meta.get_field("id_rol").db_type(connection), "integer")
        self.assertEqual(
            Parqueadero._meta.get_field("id_apto_asignado").db_type(connection),
            "integer",
        )
        self.assertEqual(
            Persona._meta.get_field("tipo_documento").db_type(connection),
            "character(2)",
        )

    def test_columnas_nuevas_de_neon(self):
        self.assertIsNotNone(Notificacion._meta.get_field("fecha_creacion"))
        self.assertEqual(Turno._meta.get_field("estado").default, "Abierto")
        self.assertTrue(RegistroAcceso._meta.get_field("celda_asignada").null)


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


class RutasApiRootTests(SimpleTestCase):
    def test_nombres_unicos_y_reversibles(self):
        self.assertEqual(len(NOMBRES_API_ROOT), len(set(NOMBRES_API_ROOT)))
        for nombre in NOMBRES_API_ROOT:
            with self.subTest(nombre=nombre):
                self.assertTrue(reverse(nombre))

    def test_no_existe_api_root_generico(self):
        with self.assertRaises(NoReverseMatch):
            reverse("api-root")
