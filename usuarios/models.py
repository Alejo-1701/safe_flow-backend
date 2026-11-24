from django.db import models


class Perfil(models.Model):
    doc_persona = models.CharField(primary_key=True, max_length=10, db_column="doc_persona")
    contrasenia = models.CharField(max_length=255)
    estado_perfil = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = "perfil"
