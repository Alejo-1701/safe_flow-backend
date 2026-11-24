from django.db import models


class PersonaVehiculoRef(models.Model):
    """
    Modelo de referencia de solo lectura hacia la tabla 'personas' en Neon.
    Permite vincular vehículos con propietarios sin tocar el módulo 'personas'.
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


class Vehiculo(models.Model):
    placa = models.CharField(primary_key=True, max_length=10)
    numero_chasis = models.CharField(unique=True, max_length=30)
    tipo = models.CharField(max_length=20)
    linea = models.CharField(max_length=50)
    modelo = models.IntegerField()
    cilindraje = models.IntegerField()
    color = models.CharField(max_length=20)
    servicio = models.CharField(max_length=20)
    clase_vehiculo = models.CharField(max_length=20)
    doc_propietario = models.ForeignKey(
        PersonaVehiculoRef,
        on_delete=models.DO_NOTHING,
        db_column='doc_propietario',
        related_name='vehiculos'
    )

    class Meta:
        managed = False
        db_table = 'vehiculos'

    def __str__(self):
        return f"{self.placa} ({self.clase_vehiculo} - {self.linea})"