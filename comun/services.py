from config.crud import CRUDService

from .models import Notificacion, NotificacionEstado


class NotificacionService(CRUDService):
    modelo = Notificacion

    @staticmethod
    def listar():
        return Notificacion.objects.all().order_by("id_notificacion")

    @staticmethod
    def obtener(pk):
        return Notificacion.objects.filter(pk=pk).first()

    @staticmethod
    def listar_no_leidos():
        return Notificacion.objects.filter(leido=False).order_by("id_notificacion")


class NotificacionEstadoService(CRUDService):
    modelo = NotificacionEstado

    @staticmethod
    def listar():
        return NotificacionEstado.objects.select_related("notificacion").order_by("id_estado_hist")

    @staticmethod
    def obtener(pk):
        return NotificacionEstado.objects.filter(pk=pk).first()

    @staticmethod
    def listar_por_notificacion(id_notificacion):
        return NotificacionEstado.objects.filter(notificacion_id=id_notificacion).order_by("id_estado_hist")
