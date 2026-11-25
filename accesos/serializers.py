from rest_framework import serializers

from .models import RegistroAcceso, Turno


class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno
        fields = [
            "id_turno",
            "fecha_turno",
            "hora_inicio",
            "hora_fin",
            "recaudo_fisico",
            "observaciones",
            "num_documento_guardia",
        ]
        read_only_fields = ["id_turno"]


class RegistroAccesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroAcceso
        fields = [
            "id_registro",
            "placa",
            "id_turno",
            "fecha_entrada",
            "hora_entrada",
            "fecha_salida",
            "hora_salida",
        ]
        read_only_fields = ["id_registro"]
