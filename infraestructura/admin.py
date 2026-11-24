from django.contrib import admin
from .models import Apartamento, Parqueadero


@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('id_apartamento', 'torre', 'numero_apto', 'doc_propietario')
    search_fields = ('torre', 'numero_apto', 'doc_propietario__num_documento')
    list_filter = ('torre',)


@admin.register(Parqueadero)
class ParqueaderoAdmin(admin.ModelAdmin):
    list_display = ('id_parqueadero', 'tipo_celda', 'estado', 'id_apto_asignado')
    search_fields = ('id_parqueadero',)
    list_filter = ('tipo_celda', 'estado')