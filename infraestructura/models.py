from django.db import models

from config.fields import FixedCharField, IntegerForeignKey


class PersonaReferencia(models.Model):
    """
    Modelo de referencia de solo lectura hacia la tabla 'personas' en Neon.
    Evita modificar la carpeta 'personas/' de otros integrantes del equipo.
    """
    num_documento = models.CharField(primary_key=True, max_length=10)
    tipo_documento = FixedCharField(max_length=2)
    primer_nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=50, blank=True, null=True)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'personas'

    def __str__(self):
        return f"{self.num_documento} - {self.primer_nombre} {self.primer_apellido}"


class Apartamento(models.Model):
    id_apartamento = models.SmallAutoField(primary_key=True)
    torre = models.CharField(max_length=10)
    numero_apto = models.CharField(max_length=10)
    doc_propietario = models.ForeignKey(
        PersonaReferencia,
        on_delete=models.DO_NOTHING,
        db_column='doc_propietario',
        related_name='apartamentos'
    )

    class Meta:
        managed = False
        db_table = 'apartamento'

    def __str__(self):
        return f"Torre {self.torre} - Apto {self.numero_apto}"


class Parqueadero(models.Model):
    id_parqueadero = models.CharField(primary_key=True, max_length=20)
    tipo_celda = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)
    id_apto_asignado = IntegerForeignKey(
        Apartamento,
        on_delete=models.DO_NOTHING,
        db_column='id_apto_asignado',
        related_name='parqueaderos',
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'parqueadero'

    def __str__(self):
        return f"Celda {self.id_parqueadero} ({self.estado})"


class AsambleaCopropietarios(models.Model):
    id_asamblea = models.SmallAutoField(primary_key=True, db_column="id_asamblea")
    numero_acta = models.CharField(max_length=20)
    fecha_reunion = models.DateField()
    art_referencia = models.CharField(max_length=30)
    des_acuerdo = models.TextField()

    class Meta:
        managed = False
        db_table = "asamblea_copropietarios"