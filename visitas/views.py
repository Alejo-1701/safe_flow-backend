from rest_framework import viewsets

from .models import AutorizacionVisita
from .serializers import AutorizacionVisitaSerializer


class AutorizacionVisitaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AutorizacionVisita.objects.all().order_by("id_autorizacion")
    serializer_class = AutorizacionVisitaSerializer
