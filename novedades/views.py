from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Incidente, Solicitud
from .serializers import IncidenteSerializer, SolicitudSerializer


class IncidenteViewSet(viewsets.ModelViewSet):
    queryset = Incidente.objects.all().order_by("id_incidente")
    serializer_class = IncidenteSerializer
    permission_classes =[AllowAny]


class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all().order_by("id_solicitud")
    serializer_class = SolicitudSerializer
    permission_classes =[AllowAny]
