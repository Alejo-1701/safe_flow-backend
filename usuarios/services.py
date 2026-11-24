from .models import Perfil


class PerfilService:
    @staticmethod
    def listar():
        return Perfil.objects.all().order_by("doc_persona")

    @staticmethod
    def obtener(pk):
        return Perfil.objects.filter(pk=pk).first()

    @staticmethod
    def listar_activos():
        return Perfil.objects.filter(estado_perfil=True).order_by("doc_persona")
