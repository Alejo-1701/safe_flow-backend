from django.db import models
from django.utils import timezone


class Notificacion(models.Model):
    id_notificacion = models.AutoField(primary_key=True, db_column="id_notificacion")
    tipo = models.CharField(max_length=30)
    mensaje = models.TextField()
    leido = models.BooleanField(default=False, null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now, db_column="fecha_creacion")
    numero_documento = models.ForeignKey(
        "personas.Persona",
        db_column="numero_documento",
        to_field="num_documento",
        on_delete=models.DO_NOTHING,
        related_name="notificaciones",
    )

    class Meta:
        managed = False
        db_table = "notificacion"


class NotificacionEstado(models.Model):
    id_estado_hist = models.AutoField(primary_key=True, db_column="id_estado_hist")
    notificacion = models.ForeignKey(
        Notificacion,
        db_column="id_notificacion",
        on_delete=models.DO_NOTHING,
        related_name="estados",
    )
    nuevo_estado = models.CharField(max_length=20)
    duracion = models.DurationField()
    fecha_cambio = models.DateField()
    hora_cambio = models.TimeField()

    class Meta:
        managed = False
        db_table = "notificacion_estados"
