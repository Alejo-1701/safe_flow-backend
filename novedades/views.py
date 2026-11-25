from rest_framework import viewsets

from .models import Incidente, Solicitud
from .serializers import IncidenteSerializer, SolicitudSerializer


class IncidenteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Incidente.objects.all().order_by("id_incidente")
    serializer_class = IncidenteSerializer


class SolicitudViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Solicitud.objects.all().order_by("id_solicitud")
    serializer_class = SolicitudSerializer
