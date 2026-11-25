from rest_framework import serializers
from .models import AutorizacionVisita


class AutorizacionVisitaSerializer(serializers.ModelSerializer):
    residente_nombre = serializers.SerializerMethodField(read_only=True)
    visitante_nombre = serializers.SerializerMethodField(read_only=True)
    vehiculo_detalle = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AutorizacionVisita
        fields = [
            'id_autorizacion',
            'fecha_programada',
            'doc_residente',
            'residente_nombre',
            'doc_visitante',
            'visitante_nombre',
            'placa_vehiculo',
            'vehiculo_detalle',
        ]
        read_only_fields = ['id_autorizacion']

    def get_residente_nombre(self, obj):
        if obj.doc_residente:
            return f"{obj.doc_residente.primer_nombre} {obj.doc_residente.primer_apellido}"
        return None

    def get_visitante_nombre(self, obj):
        if obj.doc_visitante:
            return f"{obj.doc_visitante.primer_nombre} {obj.doc_visitante.primer_apellido}"
        return None

    def get_vehiculo_detalle(self, obj):
        if obj.placa_vehiculo:
            return f"{obj.placa_vehiculo.clase_vehiculo} - {obj.placa_vehiculo.linea} ({obj.placa_vehiculo.color})"
        return "Ingreso peatonal / Sin vehículo"

    def to_internal_value(self, data):
        mutable_data = data.copy() if hasattr(data, 'copy') else dict(data)
        if 'placa_vehiculo' in mutable_data and isinstance(mutable_data['placa_vehiculo'], str):
            placa_limpia = mutable_data['placa_vehiculo'].strip().upper()
            mutable_data['placa_vehiculo'] = placa_limpia if placa_limpia else None
        return super().to_internal_value(mutable_data)