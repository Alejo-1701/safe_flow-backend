from rest_framework import serializers
from .models import AutorizacionVisita


class AutorizacionVisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutorizacionVisita
        fields = '__all__'