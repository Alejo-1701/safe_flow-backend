from django.db import models

class Incidentes(models.Model):
    id_incidente = models.AutoField(primary_key=True)
    doc_persona = models.ForeignKey(
        'personas.Persona',
        on_delete=models.RESTRICT,
        db_column='doc_persona'
    )
    descripcion = models.TextField()
    fecha_incidente = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'incidentes'
        managed = False


class Solicitud(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Aprobada', 'Aprobada'),
        ('Rechazada', 'Rechazada'),
    ]
    id_solicitud = models.AutoField(primary_key=True)
    doc_persona = models.ForeignKey(
        'personas.Persona',
        on_delete=models.RESTRICT,
        db_column='doc_persona'
    )
    descripcion = models.TextField()
    fecha_solicitud = models.DateField(auto_now_add=True)
    estado_solicitud = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')

    class Meta:
        db_table = 'solicitud'
        managed = False


class Notificacion(models.Model):
    id_notificacion = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=30)  # Acceso, Pago, Visita, Solicitud, Incidente
    mensaje = models.TextField()
    leido = models.BooleanField(default=False)
    numero_documento = models.ForeignKey(
        'personas.Persona',
        on_delete=models.RESTRICT,
        db_column='numero_documento'
    )

    class Meta:
        db_table = 'notificacion'
        managed = False


class NotificacionEstados(models.Model):
    id_estado_hist = models.AutoField(primary_key=True)
    id_notificacion = models.ForeignKey(
        Notificacion,
        on_delete=models.RESTRICT,
        db_column='id_notificacion'
    )
    nuevo_estado = models.CharField(max_length=20)
    duracion = models.DurationField()
    fecha_cambio = models.DateField(auto_now_add=True)
    hora_cambio = models.TimeField(auto_now_add=True)

    class Meta:
        db_table = 'notificacion_estados'
        managed = False