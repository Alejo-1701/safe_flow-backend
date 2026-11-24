from rest_framework import serializers

from .models import Perfil


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ["doc_persona", "contrasenia", "estado_perfil"]
        extra_kwargs = {"contrasenia": {"write_only": True}}
