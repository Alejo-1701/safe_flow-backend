from django.contrib import admin
from .models import Vehiculo


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'clase_vehiculo', 'tipo', 'linea', 'modelo', 'doc_propietario')
    search_fields = ('placa', 'numero_chasis', 'doc_propietario__num_documento')
    list_filter = ('tipo', 'clase_vehiculo', 'servicio')