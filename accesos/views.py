from rest_framework import viewsets
from .models import Turno, RegistroAcceso
from .serializers import TurnoSerializer, RegistroAccesoSerializer


class TurnoViewSet(viewsets.ModelViewSet):
    queryset = Turno.objects.select_related('num_documento_guardia').all()
    serializer_class = TurnoSerializer


class RegistroAccesoViewSet(viewsets.ModelViewSet):
    queryset = RegistroAcceso.objects.select_related('placa', 'id_turno').all()
    serializer_class = RegistroAccesoSerializer