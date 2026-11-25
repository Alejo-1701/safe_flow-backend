from rest_framework import serializers

from .models import Incidente, Solicitud


class IncidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incidente
        fields = ["id_incidente", "doc_persona", "descripcion", "fecha_incidente"]
        read_only_fields = ["id_incidente"]


class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = [
            "id_solicitud",
            "doc_persona",
            "descripcion",
            "fecha_solicitud",
            "estado_solicitud",
        ]
        read_only_fields = ["id_solicitud"]
