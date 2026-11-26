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
