from django.db import models


class AutorizacionVisita(models.Model):
    id_autorizacion = models.AutoField(primary_key=True, db_column="id_autorizacion")
    fecha_programada = models.DateField()
    doc_residente = models.ForeignKey(
        "personas.Persona",
        db_column="doc_residente",
        to_field="num_documento",
        on_delete=models.DO_NOTHING,
        related_name="autorizaciones_residente",
    )
    doc_visitante = models.ForeignKey(
        "personas.Persona",
        db_column="doc_visitante",
        to_field="num_documento",
        on_delete=models.DO_NOTHING,
        related_name="autorizaciones_visitante",
    )
    placa_vehiculo = models.ForeignKey(
        "vehiculos.Vehiculo",
        db_column="placa_vehiculo",
        to_field="placa",
        on_delete=models.DO_NOTHING,
        related_name="autorizaciones_visita",
        null=True,
        blank=True,
    )

    class Meta:
        managed = False
        db_table = "autorizacion_visita"
        verbose_name = "Autorización de Visita"
        verbose_name_plural = "Autorizaciones de Visita"

    def __str__(self):
        return f"Autorización {self.id_autorizacion} - {self.fecha_programada}"
