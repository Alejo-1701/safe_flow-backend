from decimal import Decimal

from django.db import transaction
from django.db.models import Sum
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from accesos.models import Turno

from .models import Pago, Recaudo, Tarifa
from .serializers import (
    ArqueoRequestSerializer,
    ArqueoResponseSerializer,
    PagoSerializer,
    RecaudoSerializer,
    TarifaSerializer,
)


class TarifaViewSet(viewsets.ModelViewSet):
    queryset = Tarifa.objects.all().order_by("id_tarifa")
    serializer_class = TarifaSerializer


class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all().order_by("id_pago")
    serializer_class = PagoSerializer
    http_method_names = ["get", "post", "head", "options"]

    @extend_schema(
        request=ArqueoRequestSerializer,
        responses={200: ArqueoResponseSerializer},
        summary="Arquear turno",
        description="Suma los pagos en efectivo del turno y compara con el recaudo físico reportado.",
    )
    @action(detail=False, methods=["post"], url_path="arqueo-turno")
    def arqueo_turno(self, request):
        serializer = ArqueoRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_turno = serializer.validated_data["id_turno"]
        recaudo_fisico = serializer.validated_data["recaudo_fisico"]
        observaciones = serializer.validated_data.get("observaciones")

        with transaction.atomic():
            turno = Turno.objects.select_for_update().filter(pk=id_turno).first()
            if turno is None:
                raise ValidationError("No existe el turno indicado.")

            total_sistema = (
                Pago.objects.filter(id_turno_id=id_turno, metodo_pago="Efectivo")
                .aggregate(total=Sum("monto_total"))["total"]
                or Decimal("0.00")
            )
            diferencia = recaudo_fisico - total_sistema
            estado = "Cuadrado" if diferencia == Decimal("0.00") else "Descuadre detectado"

            turno.recaudo_fisico = recaudo_fisico
            if observaciones is not None:
                turno.observaciones = observaciones
            turno.estado = estado
            turno.save(update_fields=["recaudo_fisico", "observaciones", "estado"])

        respuesta = ArqueoResponseSerializer(
            {
                "total_sistema": total_sistema,
                "recaudo_fisico": recaudo_fisico,
                "diferencia": diferencia,
                "estado": estado,
            }
        )
        return Response(respuesta.data, status=status.HTTP_200_OK)


class RecaudoViewSet(viewsets.ModelViewSet):
    queryset = Recaudo.objects.all().order_by("numero_factura")
    serializer_class = RecaudoSerializer
    http_method_names = ["get", "post", "head", "options"]
