from rest_framework import serializers

from .models import (
    Administrador,
    EmpresaVigilancia,
    GuardiaSeguridad,
    Persona,
    PersonaCorreo,
    PersonaTelefono,
    Residente,
    Rol,
)


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ["id_rol", "nombre_rol"]
        read_only_fields = ["id_rol"]


class EmpresaVigilanciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresaVigilancia
        fields = ["nit", "nombre_empresa", "rep_legal", "telefono", "email", "direccion"]


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = [
            "num_documento",
            "tipo_documento",
            "primer_nombre",
            "segundo_nombre",
            "primer_apellido",
            "segundo_apellido",
            "id_rol",
            "nit_empresa",
        ]


class PersonaTelefonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaTelefono
        fields = ["doc_persona", "telefono"]


class PersonaCorreoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaCorreo
        fields = ["doc_persona", "email"]


class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = ["numero_documento", "rol", "inicio_gestion", "fin_gestion"]


class GuardiaSeguridadSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuardiaSeguridad
        fields = ["numero_documento", "empresa"]


class ResidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Residente
        fields = ["numero_documento", "id_apartamento"]
