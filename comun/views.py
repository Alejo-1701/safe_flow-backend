from django.http import Http404
from rest_framework import viewsets

from .serializers import NotificacionEstadoSerializer, NotificacionSerializer
from .services import NotificacionEstadoService, NotificacionService


class NotificacionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificacionSerializer

    def get_queryset(self):
        return NotificacionService.listar()

    def get_object(self):
        obj = NotificacionService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj


class NotificacionEstadoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificacionEstadoSerializer

    def get_queryset(self):
        return NotificacionEstadoService.listar()

    def get_object(self):
        obj = NotificacionEstadoService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj
