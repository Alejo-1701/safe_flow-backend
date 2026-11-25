from rest_framework import viewsets
from .models import AutorizacionVisita
from .serializers import AutorizacionVisitaSerializer


class AutorizacionVisitaViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para autorizaciones de visitas.
    Filtros disponibles: ?fecha_programada=YYYY-MM-DD, ?doc_residente=123, ?doc_visitante=456, ?placa_vehiculo=ABC123
    """
    serializer_class = AutorizacionVisitaSerializer

    def get_queryset(self):
        queryset = AutorizacionVisita.objects.select_related(
            'doc_residente', 'doc_visitante', 'placa_vehiculo'
        ).all().order_by('-fecha_programada', '-id_autorizacion')

        fecha_programada = self.request.query_params.get('fecha_programada')
        doc_residente = self.request.query_params.get('doc_residente')
        doc_visitante = self.request.query_params.get('doc_visitante')
        placa_vehiculo = self.request.query_params.get('placa_vehiculo')

        if fecha_programada:
            queryset = queryset.filter(fecha_programada=fecha_programada)
        if doc_residente:
            queryset = queryset.filter(doc_residente=doc_residente)
        if doc_visitante:
            queryset = queryset.filter(doc_visitante=doc_visitante)
        if placa_vehiculo:
            queryset = queryset.filter(placa_vehiculo__placa__iexact=placa_vehiculo.strip())

        return queryset