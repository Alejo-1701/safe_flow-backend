from rest_framework import serializers

from .models import AutorizacionVisita


class AutorizacionVisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutorizacionVisita
        fields = [
            "id_autorizacion",
            "fecha_programada",
            "doc_residente",
            "doc_visitante",
            "placa_vehiculo",
        ]
        read_only_fields = ["id_autorizacion"]
