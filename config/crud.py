from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist
from django.db import IntegrityError, models
from rest_framework.exceptions import ValidationError

try:
    from rest_framework.exceptions import Conflict
except ImportError:
    from rest_framework.exceptions import APIException
    from rest_framework.status import HTTP_409_CONFLICT

    class Conflict(APIException):
        status_code = HTTP_409_CONFLICT
        default_detail = "Conflicto de integridad de datos."
        default_code = "conflict"


class CRUDService:
    modelo = None

    @classmethod
    def preparar(cls, datos):
        valores = dict(datos)
        for nombre, valor in list(valores.items()):
            try:
                campo = cls.modelo._meta.get_field(nombre)
            except FieldDoesNotExist:
                continue
            if not campo.is_relation or valor is None or isinstance(valor, models.Model):
                continue
            try:
                valores[nombre] = campo.related_model._default_manager.get(
                    **{campo.target_field.name: valor}
                )
            except ObjectDoesNotExist as error:
                raise ValidationError(
                    f"No existe {campo.related_model.__name__} con {campo.target_field.name}={valor}."
                ) from error
        return valores

    @classmethod
    def crear(cls, datos):
        try:
            return cls.modelo.objects.create(**cls.preparar(datos))
        except IntegrityError as error:
            raise ValidationError(
                f"No se pudo crear el registro de {cls.modelo.__name__}. "
                "Revise los datos enviados y las restricciones de la base de datos."
            ) from error

    @classmethod
    def actualizar(cls, instancia, datos):
        valores = cls.preparar(datos)
        valores.pop(cls.modelo._meta.pk.name, None)
        for campo, valor in valores.items():
            setattr(instancia, campo, valor)
        try:
            instancia.save()
        except IntegrityError as error:
            raise ValidationError(
                f"No se pudo actualizar el registro de {cls.modelo.__name__}. "
                "Revise los datos enviados y las restricciones de la base de datos."
            ) from error
        return instancia

    @classmethod
    def eliminar(cls, instancia):
        try:
            return instancia.delete()
        except IntegrityError as error:
            raise Conflict(
                f"No se pudo eliminar el registro de {cls.modelo.__name__} "
                "porque existen registros dependientes o restricciones de integridad."
            ) from error
