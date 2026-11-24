from rest_framework import viewsets
from .models import AutorizacionVisita
from .serializers import AutorizacionVisitaSerializer


class AutorizacionVisitaViewSet(viewsets.ModelViewSet):
    queryset = AutorizacionVisita.objects.select_related(
        'doc_residente', 'doc_visitante', 'placa_vehiculo'
    ).all()
    serializer_class = AutorizacionVisitaSerializer