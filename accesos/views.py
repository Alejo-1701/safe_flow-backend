from rest_framework import viewsets

from .models import RegistroAcceso, Turno
from .serializers import RegistroAccesoSerializer, TurnoSerializer


class TurnoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Turno.objects.all().order_by("id_turno")
    serializer_class = TurnoSerializer


class RegistroAccesoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RegistroAcceso.objects.all().order_by("id_registro")
    serializer_class = RegistroAccesoSerializer
