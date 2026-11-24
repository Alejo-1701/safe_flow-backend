from django.db import models


class Turno(models.Model):
    id_turno = models.SmallAutoField(primary_key=True)
    fecha_turno = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    recaudo_fisico = models.DecimalField(max_digits=12, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)
    num_documento_guardia = models.ForeignKey(
        'personas.Persona',
        on_delete=models.RESTRICT,
        db_column='num_documento_guardia',
        related_name='turnos',
    )

    class Meta:
        db_table = 'turno'
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'

    def __str__(self):
        return f'Turno {self.id_turno} – {self.fecha_turno}'


class RegistroAcceso(models.Model):
    id_registro = models.SmallAutoField(primary_key=True)
    placa = models.ForeignKey(
        'vehiculos.Vehiculo',
        on_delete=models.RESTRICT,
        db_column='placa',
        to_field='placa',
        related_name='registros_acceso',
    )
    id_turno = models.ForeignKey(
        Turno,
        on_delete=models.RESTRICT,
        db_column='id_turno',
        related_name='registros_acceso',
    )
    fecha_entrada = models.DateField()
    hora_entrada = models.TimeField()
    fecha_salida = models.DateField(blank=True, null=True)
    hora_salida = models.TimeField(blank=True, null=True)

    class Meta:
        db_table = 'registro_acceso'
        verbose_name = 'Registro de Acceso'
        verbose_name_plural = 'Registros de Acceso'

    def __str__(self):
        return f'Registro {self.id_registro} – Placa {self.placa_id}'