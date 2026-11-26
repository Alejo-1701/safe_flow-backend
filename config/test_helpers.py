from datetime import date, time
from decimal import Decimal

from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.db import connection
from rest_framework.test import APITestCase

MODELS_EN_ORDEN = [
    "personas.Rol",
    "personas.EmpresaVigilancia",
    "personas.Persona",
    "personas.PersonaTelefono",
    "personas.PersonaCorreo",
    "usuarios.Perfil",
    "vehiculos.Vehiculo",
    "infraestructura.Apartamento",
    "infraestructura.Parqueadero",
    "infraestructura.AsambleaCopropietarios",
    "accesos.Turno",
    "accesos.RegistroAcceso",
    "financiero.Pago",
    "financiero.Tarifa",
    "financiero.Recaudo",
    "comun.Notificacion",
    "comun.NotificacionEstado",
    "novedades.Incidente",
    "novedades.Solicitud",
    "visitas.AutorizacionVisita",
]


def crear_tablas_no_gestionadas():
    """Crea en SQLite las tablas de los modelos managed=False usados por los tests."""
    existentes = set(connection.introspection.table_names())
    with connection.schema_editor() as editor:
        for etiqueta in MODELS_EN_ORDEN:
            modelo = apps.get_model(etiqueta)
            tabla = modelo._meta.db_table
            if tabla in existentes:
                continue
            editor.create_model(modelo)
            existentes.add(tabla)


class ApiTestCaseBase(APITestCase):
    @classmethod
    def setUpClass(cls):
        # SQLite no permite crear tablas con FK dentro de la transacción de TestCase.
        crear_tablas_no_gestionadas()
        super().setUpClass()


def crear_rol(nombre="Residente"):
    rol, _ = apps.get_model("personas", "Rol").objects.get_or_create(
        id_rol=1, defaults={"nombre_rol": nombre}
    )
    return rol


def crear_persona(num_documento="10000001"):
    rol = crear_rol()
    persona, _ = apps.get_model("personas", "Persona").objects.get_or_create(
        num_documento=num_documento,
        defaults={
            "tipo_documento": "CC",
            "primer_nombre": "Ana",
            "segundo_nombre": "María",
            "primer_apellido": "Pérez",
            "segundo_apellido": "López",
            "id_rol": rol,
        },
    )
    return persona


def crear_vehiculo(num_documento="10000001", placa="ABC123"):
    return apps.get_model("vehiculos", "Vehiculo").objects.create(
        placa=placa,
        numero_chasis=f"CH-{placa}",
        tipo="Carro",
        linea="Corolla",
        modelo=2020,
        cilindraje=1800,
        color="Rojo",
        servicio="Particular",
        clase_vehiculo="Carro",
        doc_propietario_id=num_documento,
    )


def crear_turno(num_documento="10000001"):
    persona = apps.get_model("personas", "Persona").objects.filter(
        num_documento=num_documento
    ).first() or crear_persona(num_documento)
    return apps.get_model("accesos", "Turno").objects.create(
        fecha_turno=date.today(),
        hora_inicio=time(8, 0),
        hora_fin=time(16, 0),
        recaudo_fisico=Decimal("0.00"),
        num_documento_guardia=persona,
    )


def crear_registro(placa="ABC123", id_turno=None):
    turno = id_turno or crear_turno()
    vehiculo = apps.get_model("vehiculos", "Vehiculo").objects.filter(
        placa=placa
    ).first() or crear_vehiculo(placa=placa)
    return apps.get_model("accesos", "RegistroAcceso").objects.create(
        placa=vehiculo,
        id_turno=turno,
        fecha_entrada=date.today(),
        hora_entrada=time(10, 0),
    )


def crear_celda(id_parqueadero="P-01", estado="Disponible"):
    return apps.get_model("infraestructura", "Parqueadero").objects.create(
        id_parqueadero=id_parqueadero,
        tipo_celda="Carro",
        estado=estado,
    )


def crear_perfil(num_documento="10000001", contrasenia="Clave123", estado=True, hash_contrasenia=True):
    crear_persona(num_documento)
    return apps.get_model("usuarios", "Perfil").objects.create(
        doc_persona_id=num_documento,
        contrasenia=make_password(contrasenia) if hash_contrasenia else contrasenia,
        estado_perfil=estado,
    )


def crear_asamblea():
    return apps.get_model("infraestructura", "AsambleaCopropietarios").objects.create(
        numero_acta="ACT-001",
        fecha_reunion=date.today(),
        art_referencia="Art. 5",
        des_acuerdo="Acuerdo de prueba",
    )


def crear_tarifa():
    return apps.get_model("financiero", "Tarifa").objects.create(
        tipo_vehiculo="Carro",
        valor_minuto=Decimal("50.00"),
        id_asamblea=crear_asamblea(),
    )


def crear_pago(monto, id_turno=None, metodo_pago="Efectivo"):
    registro = crear_registro(id_turno=id_turno)
    return apps.get_model("financiero", "Pago").objects.create(
        metodo_pago=metodo_pago,
        fecha_caja=date.today(),
        hora_caja=time(12, 0),
        monto_total=Decimal(str(monto)),
        id_registro=registro,
        id_turno=registro.id_turno,
    )


def crear_solicitud(num_documento="10000001", estado="Pendiente"):
    crear_persona(num_documento)
    return apps.get_model("novedades", "Solicitud").objects.create(
        doc_persona_id=num_documento,
        descripcion="Solicitud de prueba",
        fecha_solicitud=date.today(),
        estado_solicitud=estado,
    )


def crear_telefono(num_documento="10000001", telefono="3001234567"):
    crear_persona(num_documento)
    return apps.get_model("personas", "PersonaTelefono").objects.create(
        doc_persona_id=num_documento,
        telefono=telefono,
    )


def crear_correo(num_documento="10000001", email="ana@example.com"):
    crear_persona(num_documento)
    return apps.get_model("personas", "PersonaCorreo").objects.create(
        doc_persona_id=num_documento,
        email=email,
    )


def crear_notificacion(num_documento="10000001", tipo="Aviso", mensaje="Mensaje de prueba"):
    crear_persona(num_documento)
    return apps.get_model("comun", "Notificacion").objects.create(
        tipo=tipo,
        mensaje=mensaje,
        numero_documento_id=num_documento,
    )
