from django.db import models


class PersonaVisitaRef(models.Model):
    """
    Modelo de referencia de solo lectura hacia la tabla 'personas' en Neon.
    Permite vincular residentes y visitantes sin depender de la carpeta 'personas/'.
    """
    num_documento = models.CharField(primary_key=True, max_length=10)
    tipo_documento = models.CharField(max_length=2)
    primer_nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=50, blank=True, null=True)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'personas'

    def __str__(self):
        return f"{self.num_documento} - {self.primer_nombre} {self.primer_apellido}"


class AutorizacionVisita(models.Model):
    id_autorizacion = models.AutoField(primary_key=True)
    fecha_programada = models.DateField()
    doc_residente = models.ForeignKey(
        PersonaVisitaRef,
        on_delete=models.DO_NOTHING,
        db_column='doc_residente',
        related_name='autorizaciones_emitidas',
    )
    doc_visitante = models.ForeignKey(
        PersonaVisitaRef,
        on_delete=models.DO_NOTHING,
        db_column='doc_visitante',
        related_name='autorizaciones_recibidas',
    )
    placa_vehiculo = models.ForeignKey(
        'vehiculos.Vehiculo',
        on_delete=models.DO_NOTHING,
        db_column='placa_vehiculo',
        to_field='placa',
        related_name='autorizaciones_visita',
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = 'autorizacion_visita'
        verbose_name = 'Autorización de Visita'
        verbose_name_plural = 'Autorizaciones de Visita'

    def __str__(self):
        return f'Autorización {self.id_autorizacion} – {self.fecha_programada}'