from django.contrib import admin
from .models import AutorizacionVisita


@admin.register(AutorizacionVisita)
class AutorizacionVisitaAdmin(admin.ModelAdmin):
    list_display = ('id_autorizacion', 'fecha_programada', 'doc_residente', 'doc_visitante', 'placa_vehiculo')
    list_filter = ('fecha_programada',)
    search_fields = (
        'doc_residente__num_documento',
        'doc_visitante__num_documento',
        'placa_vehiculo__placa',
    )