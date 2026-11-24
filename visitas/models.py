from django.db import models


class AutorizacionVisita(models.Model):
    id_autorizacion = models.AutoField(primary_key=True)
    fecha_programada = models.DateField()
    doc_residente = models.ForeignKey(
        'personas.Persona',
        on_delete=models.CASCADE,
        db_column='doc_residente',
        related_name='autorizaciones_emitidas',
    )
    doc_visitante = models.ForeignKey(
        'personas.Persona',
        on_delete=models.CASCADE,
        db_column='doc_visitante',
        related_name='autorizaciones_recibidas',
    )
    placa_vehiculo = models.ForeignKey(
        'vehiculos.Vehiculo',
        on_delete=models.SET_NULL,
        db_column='placa_vehiculo',
        to_field='placa',
        related_name='autorizaciones_visita',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'autorizacion_visita'
        verbose_name = 'Autorización de Visita'
        verbose_name_plural = 'Autorizaciones de Visita'

    def __str__(self):
        return f'Autorización {self.id_autorizacion} – {self.fecha_programada}'