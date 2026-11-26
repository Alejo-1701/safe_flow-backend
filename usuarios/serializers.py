from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Perfil


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ["doc_persona", "contrasenia", "estado_perfil"]
        extra_kwargs = {"contrasenia": {"write_only": True}}

    def validate_contrasenia(self, value):
        validate_password(value)
        return value


class LoginRequestSerializer(serializers.Serializer):
    num_documento = serializers.CharField(max_length=10)
    contrasenia = serializers.CharField(write_only=True, max_length=255)


class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    num_documento = serializers.CharField(read_only=True)
    nombre_completo = serializers.CharField(read_only=True)
    rol = serializers.CharField(read_only=True)
