from rest_framework import serializers
from .models import Incidentes, Solicitud, Notificacion, NotificacionEstados

class IncidentesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incidentes
        fields = '__all__'

class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = '__all__'

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = '__all__'