from rest_framework import serializers
from .models import Apartamento, AsambleaCopropietarios, Parqueadero


class ApartamentoSerializer(serializers.ModelSerializer):
    propietario_nombre = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Apartamento
        fields = [
            'id_apartamento',
            'torre',
            'numero_apto',
            'doc_propietario',
            'propietario_nombre',
        ]
        read_only_fields = ['id_apartamento']

    def get_propietario_nombre(self, obj):
        if obj.doc_propietario:
            return f"{obj.doc_propietario.primer_nombre} {obj.doc_propietario.primer_apellido}"
        return None


class ParqueaderoSerializer(serializers.ModelSerializer):
    apartamento_detalle = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Parqueadero
        fields = [
            'id_parqueadero',
            'tipo_celda',
            'estado',
            'id_apto_asignado',
            'apartamento_detalle',
        ]

    def get_apartamento_detalle(self, obj):
        if obj.id_apto_asignado:
            return f"Torre {obj.id_apto_asignado.torre} - Apto {obj.id_apto_asignado.numero_apto}"
        return "Sin asignar / Visitantes"

    def validate_id_parqueadero(self, value):
        return value.strip().upper()


class AsambleaCopropietariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsambleaCopropietarios
        fields = ["id_asamblea", "numero_acta", "fecha_reunion", "art_referencia", "des_acuerdo"]
        read_only_fields = ["id_asamblea"]