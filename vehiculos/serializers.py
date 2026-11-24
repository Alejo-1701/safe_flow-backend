from rest_framework import serializers
from .models import Vehiculo


class VehiculoSerializer(serializers.ModelSerializer):
    propietario_nombre = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Vehiculo
        fields = [
            'placa',
            'numero_chasis',
            'tipo',
            'linea',
            'modelo',
            'cilindraje',
            'color',
            'servicio',
            'clase_vehiculo',
            'doc_propietario',
            'propietario_nombre',
        ]

    def get_propietario_nombre(self, obj):
        if obj.doc_propietario:
            return f"{obj.doc_propietario.primer_nombre} {obj.doc_propietario.primer_apellido}"
        return None

    def validate_placa(self, value):
        return value.strip().upper()

    def validate_numero_chasis(self, value):
        return value.strip().upper()