from rest_framework import serializers

from .models import RegistroAcceso, Turno


class TurnoSerializer(serializers.ModelSerializer):
    guardia_nombre = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Turno
        fields = [
            "id_turno",
            "fecha_turno",
            "hora_inicio",
            "hora_fin",
            "recaudo_fisico",
            "observaciones",
            "estado",
            "num_documento_guardia",
            "guardia_nombre",
        ]
        read_only_fields = ["id_turno", "estado"]

    def get_guardia_nombre(self, obj) -> str | None:
        if obj.num_documento_guardia:
            return f"{obj.num_documento_guardia.primer_nombre} {obj.num_documento_guardia.primer_apellido}"
        return None


class RegistroAccesoSerializer(serializers.ModelSerializer):
    vehiculo_detalle = serializers.SerializerMethodField(read_only=True)
    en_parqueadero = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RegistroAcceso
        fields = [
            "id_registro",
            "placa",
            "vehiculo_detalle",
            "id_turno",
            "fecha_entrada",
            "hora_entrada",
            "fecha_salida",
            "hora_salida",
            "celda_asignada",
            "en_parqueadero",
        ]
        read_only_fields = ["id_registro", "celda_asignada"]

    def get_vehiculo_detalle(self, obj) -> str | None:
        if obj.placa:
            return f"{obj.placa.clase_vehiculo} - {obj.placa.linea} ({obj.placa.color})"
        return None

    def get_en_parqueadero(self, obj) -> bool:
        return obj.fecha_salida is None and obj.hora_salida is None

    def to_internal_value(self, data):
        mutable_data = data.copy() if hasattr(data, "copy") else dict(data)
        if "placa" in mutable_data and isinstance(mutable_data["placa"], str):
            mutable_data["placa"] = mutable_data["placa"].strip().upper()
        return super().to_internal_value(mutable_data)


class IngresoRequestSerializer(serializers.Serializer):
    placa = serializers.CharField(max_length=10)
    id_turno = serializers.IntegerField()


class IngresoResponseSerializer(serializers.Serializer):
    id_registro = serializers.IntegerField()
    celda_asignada = serializers.CharField(max_length=20)
    mensaje = serializers.CharField()
