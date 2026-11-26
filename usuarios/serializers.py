from rest_framework import serializers

from .models import Perfil


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ["doc_persona", "contrasenia", "estado_perfil"]
        extra_kwargs = {"contrasenia": {"write_only": True}}


class LoginRequestSerializer(serializers.Serializer):
    num_documento = serializers.CharField(max_length=10)
    contrasenia = serializers.CharField(write_only=True)


class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    num_documento = serializers.CharField()
    nombre_completo = serializers.CharField()
    rol = serializers.CharField()
