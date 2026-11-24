from rest_framework import serializers

from .models import Notificacion, NotificacionEstado


class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ["id_notificacion", "tipo", "mensaje", "leido", "numero_documento"]
        read_only_fields = ["id_notificacion"]


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
        read_only_fields = ["id_estado_hist", "fecha_cambio", "hora_cambio"]
