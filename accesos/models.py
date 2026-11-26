from django.db import models


class Turno(models.Model):
    id_turno = models.SmallAutoField(primary_key=True, db_column="id_turno")
    fecha_turno = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    recaudo_fisico = models.DecimalField(max_digits=12, decimal_places=2)
    observaciones = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=30, default="Abierto")
    num_documento_guardia = models.ForeignKey(
        "personas.Persona",
        db_column="num_documento_guardia",
        to_field="num_documento",
        on_delete=models.DO_NOTHING,
        related_name="turnos",
    )

    class Meta:
        managed = False
        db_table = "turno"
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"

    def __str__(self):
        return f"Turno {self.id_turno} - {self.fecha_turno}"


class RegistroAcceso(models.Model):
    id_registro = models.SmallAutoField(primary_key=True, db_column="id_registro")
    placa = models.ForeignKey(
        "vehiculos.Vehiculo",
        db_column="placa",
        to_field="placa",
        on_delete=models.DO_NOTHING,
        related_name="registros_acceso_vehiculo",
    )
    id_turno = models.ForeignKey(
        "accesos.Turno",
        db_column="id_turno",
        to_field="id_turno",
        on_delete=models.DO_NOTHING,
        related_name="registros_acceso",
    )
    fecha_entrada = models.DateField()
    hora_entrada = models.TimeField()
    fecha_salida = models.DateField(null=True, blank=True)
    hora_salida = models.TimeField(null=True, blank=True)
    celda_asignada = models.ForeignKey(
        "infraestructura.Parqueadero",
        db_column="celda_asignada",
        to_field="id_parqueadero",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="ingresos",
    )

    class Meta:
        managed = False
        db_table = "registro_acceso"
        verbose_name = "Registro de Acceso"
        verbose_name_plural = "Registros de Acceso"

    def __str__(self):
        return f"Registro {self.id_registro} - Placa {self.placa_id}"
