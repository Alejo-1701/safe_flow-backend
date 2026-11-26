from rest_framework import serializers

from .models import Pago, Recaudo, Tarifa


class TarifaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarifa
        fields = ["id_tarifa", "tipo_vehiculo", "valor_minuto", "id_asamblea"]
        read_only_fields = ["id_tarifa"]


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = [
            "id_pago",
            "metodo_pago",
            "fecha_caja",
            "hora_caja",
            "monto_total",
            "id_registro",
            "id_turno",
        ]
        read_only_fields = ["id_pago"]


class RecaudoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recaudo
        fields = [
            "numero_factura",
            "id_pago",
            "id_tarifa",
            "id_confirmacion",
            "sub_total",
            "total_pagado",
        ]
        read_only_fields = ["numero_factura"]


class ArqueoRequestSerializer(serializers.Serializer):
    id_turno = serializers.IntegerField()
    recaudo_fisico = serializers.DecimalField(max_digits=12, decimal_places=2)
    observaciones = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )


class ArqueoResponseSerializer(serializers.Serializer):
    total_sistema = serializers.DecimalField(max_digits=12, decimal_places=2)
    recaudo_fisico = serializers.DecimalField(max_digits=12, decimal_places=2)
    diferencia = serializers.DecimalField(max_digits=12, decimal_places=2)
    estado = serializers.CharField(max_length=30)
