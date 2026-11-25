from django.shortcuts import render
from decimal import Decimal
from datetime import datetime
from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AsambleaCopropietarios, Tarifa, Pago, Recaudo
from .serializers import AsambleaSerializer, TarifaSerializer, PagoSerializer, RecaudoSerializer

class AsambleaViewSet(viewsets.ModelViewSet):
    queryset = AsambleaCopropietarios.objects.all()
    serializer_class = AsambleaSerializer

class TarifaViewSet(viewsets.ModelViewSet):
    queryset = Tarifa.objects.all()
    serializer_class = TarifaSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

    # POST /api/pagos/arqueo-turno/
    @action(detail=False, methods=['post'], url_path='arqueo-turno')
    def arqueo_turno(self, request):
        id_turno = request.data.get('id_turno')
        dinero_fisico = Decimal(str(request.data.get('recaudo_fisico', 0)))

        total_sistema = Pago.objects.filter(
            id_turno=id_turno,
            metodo_pago__iexact='Efectivo'
        ).aggregate(total=Sum('monto_total'))['total'] or Decimal('0.00')

        diferencia = dinero_fisico - total_sistema
        return Response({
            "id_turno": id_turno,
            "total_sistema": total_sistema,
            "recaudo_fisico": dinero_fisico,
            "diferencia": diferencia,
            "estado": "Cuadrado" if diferencia == 0 else "Descuadre detectado"
        })

class RecaudoViewSet(viewsets.ModelViewSet):
    queryset = Recaudo.objects.all()
    serializer_class = RecaudoSerializer