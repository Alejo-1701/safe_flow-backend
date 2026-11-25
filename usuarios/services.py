from django.contrib.auth.hashers import make_password

from config.crud import CRUDService

from .models import Perfil


class PerfilService(CRUDService):
    modelo = Perfil

    @classmethod
    def crear(cls, datos):
        valores = dict(datos)
        if "contrasenia" in valores:
            valores["contrasenia"] = make_password(valores["contrasenia"])
        return super().crear(valores)

    @classmethod
    def actualizar(cls, instancia, datos):
        valores = dict(datos)
        if "contrasenia" in valores:
            valores["contrasenia"] = make_password(valores["contrasenia"])
        return super().actualizar(instancia, valores)

    @staticmethod
    def listar():
        return Perfil.objects.all().order_by("doc_persona")

    @staticmethod
    def obtener(pk):
        return Perfil.objects.filter(pk=pk).first()

    @staticmethod
    def listar_activos():
        return Perfil.objects.filter(estado_perfil=True).order_by("doc_persona")
