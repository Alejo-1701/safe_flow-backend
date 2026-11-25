from django.db import models


class Perfil(models.Model):
    doc_persona = models.ForeignKey(
        "personas.Persona",
        primary_key=True,
        db_column="doc_persona",
        to_field="num_documento",
        on_delete=models.DO_NOTHING,
        related_name="perfil",
    )
    contrasenia = models.CharField(max_length=255)
    estado_perfil = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "perfil"
