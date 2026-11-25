from rest_framework import serializers
from .models import AsambleaCopropietarios, Tarifa, Pago, Recaudo

class AsambleaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsambleaCopropietarios
        fields = '__all__'

class TarifaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarifa
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

class RecaudoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recaudo
        fields = '__all__'