from rest_framework import viewsets

from .models import Pago, Recaudo, Tarifa
from .serializers import PagoSerializer, RecaudoSerializer, TarifaSerializer


class TarifaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tarifa.objects.all().order_by("id_tarifa")
    serializer_class = TarifaSerializer


class PagoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pago.objects.all().order_by("id_pago")
    serializer_class = PagoSerializer


class RecaudoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recaudo.objects.all().order_by("numero_factura")
    serializer_class = RecaudoSerializer
