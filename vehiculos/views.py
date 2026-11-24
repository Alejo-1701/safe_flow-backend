from rest_framework import viewsets
from .models import Vehiculo
from .serializers import VehiculoSerializer


class VehiculoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para la gestión de vehículos en SafeFlow.
    Permite filtrar por ?doc_propietario=12345 o ?tipo=Carro en la URL.
    """
    serializer_class = VehiculoSerializer

    def get_queryset(self):
        queryset = Vehiculo.objects.select_related('doc_propietario').all().order_by('placa')
        doc_propietario = self.request.query_params.get('doc_propietario')
        tipo = self.request.query_params.get('tipo')

        if doc_propietario:
            queryset = queryset.filter(doc_propietario=doc_propietario)
        if tipo:
            queryset = queryset.filter(tipo__iexact=tipo)

        return queryset