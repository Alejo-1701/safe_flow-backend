from rest_framework import serializers

from .models import Notificacion, NotificacionEstado


class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = [
            "id_notificacion",
            "tipo",
            "mensaje",
            "leido",
            "fecha_creacion",
            "numero_documento",
        ]
        read_only_fields = ["id_notificacion", "fecha_creacion"]


class NotificacionEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificacionEstado
        fields = [
            "id_estado_hist",
            "notificacion",
            "nuevo_estado",
            "duracion",
            "fecha_cambio",
            "hora_cambio",
        ]
        read_only_fields = ["id_estado_hist"]
