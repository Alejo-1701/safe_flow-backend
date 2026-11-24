from rest_framework import viewsets
from .models import Apartamento, Parqueadero
from .serializers import ApartamentoSerializer, ParqueaderoSerializer


class ApartamentoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para apartamentos del conjunto residencial.
    Filtros disponibles: ?torre=A y ?doc_propietario=12345
    """
    serializer_class = ApartamentoSerializer

    def get_queryset(self):
        queryset = Apartamento.objects.select_related('doc_propietario').all().order_by('torre', 'numero_apto')
        torre = self.request.query_params.get('torre')
        doc_propietario = self.request.query_params.get('doc_propietario')

        if torre:
            queryset = queryset.filter(torre__iexact=torre)
        if doc_propietario:
            queryset = queryset.filter(doc_propietario=doc_propietario)

        return queryset


class ParqueaderoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para celdas de parqueadero.
    Filtros disponibles: ?estado=Disponible y ?tipo_celda=Carro
    """
    serializer_class = ParqueaderoSerializer

    def get_queryset(self):
        queryset = Parqueadero.objects.select_related('id_apto_asignado').all().order_by('id_parqueadero')
        estado = self.request.query_params.get('estado')
        tipo_celda = self.request.query_params.get('tipo_celda')

        if estado:
            queryset = queryset.filter(estado__iexact=estado)
        if tipo_celda:
            queryset = queryset.filter(tipo_celda__iexact=tipo_celda)

        return queryset