from django.db import models


class Incidente(models.Model):
    id_incidente = models.AutoField(primary_key=True, db_column="id_incidente")
    doc_persona = models.ForeignKey(
        "personas.Persona",
        db_column="doc_persona",
        to_field="num_documento",
        on_delete=models.DO_NOTHING,
        related_name="incidentes",
    )
    descripcion = models.TextField()
    fecha_incidente = models.DateField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "incidentes"


class Solicitud(models.Model):
    id_solicitud = models.AutoField(primary_key=True, db_column="id_solicitud")
    doc_persona = models.ForeignKey(
        "personas.Persona",
        db_column="doc_persona",
        to_field="num_documento",
        on_delete=models.DO_NOTHING,
        related_name="solicitudes",
    )
    descripcion = models.TextField()
    fecha_solicitud = models.DateField()
    estado_solicitud = models.CharField(max_length=20, default="Pendiente")

    class Meta:
        managed = False
        db_table = "solicitud"
