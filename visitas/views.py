from rest_framework import viewsets

from .models import AutorizacionVisita
from .serializers import AutorizacionVisitaSerializer


class AutorizacionVisitaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AutorizacionVisitaSerializer

    def get_queryset(self):
        queryset = AutorizacionVisita.objects.select_related(
            "doc_residente", "doc_visitante", "placa_vehiculo"
        ).all().order_by("-fecha_programada", "-id_autorizacion")

        fecha_programada = self.request.query_params.get("fecha_programada")
        doc_residente = self.request.query_params.get("doc_residente")
        doc_visitante = self.request.query_params.get("doc_visitante")
        placa_vehiculo = self.request.query_params.get("placa_vehiculo")

        if fecha_programada:
            queryset = queryset.filter(fecha_programada=fecha_programada)
        if doc_residente:
            queryset = queryset.filter(doc_residente=doc_residente)
        if doc_visitante:
            queryset = queryset.filter(doc_visitante=doc_visitante)
        if placa_vehiculo:
            queryset = queryset.filter(placa_vehiculo__placa__iexact=placa_vehiculo.strip())

        return queryset
