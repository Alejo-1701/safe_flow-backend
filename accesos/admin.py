from django.contrib import admin
from .models import Turno, RegistroAcceso


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('id_turno', 'fecha_turno', 'hora_inicio', 'hora_fin', 'num_documento_guardia', 'recaudo_fisico')
    list_filter = ('fecha_turno',)
    search_fields = ('num_documento_guardia__num_documento',)


@admin.register(RegistroAcceso)
class RegistroAccesoAdmin(admin.ModelAdmin):
    list_display = ('id_registro', 'placa', 'id_turno', 'fecha_entrada', 'hora_entrada', 'fecha_salida', 'hora_salida')
    list_filter = ('fecha_entrada',)
    search_fields = ('placa__placa',)