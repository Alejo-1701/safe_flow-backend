from rest_framework import viewsets

from .models import Notificacion, NotificacionEstado
from .serializers import NotificacionEstadoSerializer, NotificacionSerializer


class NotificacionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer


class NotificacionEstadoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NotificacionEstado.objects.all()
    serializer_class = NotificacionEstadoSerializer
