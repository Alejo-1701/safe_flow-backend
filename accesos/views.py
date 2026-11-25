from rest_framework import viewsets
from .models import Turno, RegistroAcceso
from .serializers import TurnoSerializer, RegistroAccesoSerializer


class TurnoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para turnos de vigilancia.
    Filtros disponibles: ?fecha_turno=YYYY-MM-DD y ?num_documento_guardia=123456
    """
    serializer_class = TurnoSerializer

    def get_queryset(self):
        queryset = Turno.objects.select_related('num_documento_guardia').all().order_by('-fecha_turno', '-id_turno')
        fecha_turno = self.request.query_params.get('fecha_turno')
        guardia = self.request.query_params.get('num_documento_guardia')

        if fecha_turno:
            queryset = queryset.filter(fecha_turno=fecha_turno)
        if guardia:
            queryset = queryset.filter(num_documento_guardia=guardia)

        return queryset


class RegistroAccesoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para entradas y salidas de vehículos.
    Filtros disponibles: ?placa=ABC123, ?id_turno=1, ?fecha_entrada=YYYY-MM-DD, ?en_parqueadero=true
    """
    serializer_class = RegistroAccesoSerializer

    def get_queryset(self):
        queryset = RegistroAcceso.objects.select_related('placa', 'id_turno').all().order_by('-id_registro')
        placa = self.request.query_params.get('placa')
        id_turno = self.request.query_params.get('id_turno')
        fecha_entrada = self.request.query_params.get('fecha_entrada')
        en_parqueadero = self.request.query_params.get('en_parqueadero')

        if placa:
            queryset = queryset.filter(placa__placa__iexact=placa.strip())
        if id_turno:
            queryset = queryset.filter(id_turno=id_turno)
        if fecha_entrada:
            queryset = queryset.filter(fecha_entrada=fecha_entrada)
        if en_parqueadero and en_parqueadero.lower() == 'true':
            queryset = queryset.filter(fecha_salida__isnull=True, hora_salida__isnull=True)

        return queryset