from django.db import models


class Rol(models.Model):
    id_rol = models.SmallAutoField(primary_key=True, db_column="id_rol")
    nombre_rol = models.CharField(max_length=15, unique=True)

    class Meta:
        managed = False
        db_table = "roles"


class EmpresaVigilancia(models.Model):
    nit = models.CharField(primary_key=True, max_length=20, db_column="nit")
    nombre_empresa = models.CharField(max_length=100)
    rep_legal = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "empresa_vigilancia"


class Persona(models.Model):
    num_documento = models.CharField(primary_key=True, max_length=10, db_column="num_documento")
    tipo_documento = models.CharField(max_length=2)
    primer_nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=50, null=True, blank=True)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50)
    id_rol = models.ForeignKey(
        Rol,
        db_column="id_rol",
        to_field="id_rol",
        on_delete=models.DO_NOTHING,
        related_name="personas",
    )
    nit_empresa = models.ForeignKey(
        EmpresaVigilancia,
        db_column="nit_empresa",
        to_field="nit",
        on_delete=models.DO_NOTHING,
        related_name="personas",
        null=True,
        blank=True,
    )

    class Meta:
        managed = False
        db_table = "personas"


class PersonaTelefono(models.Model):
    doc_persona = models.ForeignKey(
        Persona,
        db_column="doc_persona",
        to_field="num_documento",
        on_delete=models.DO_NOTHING,
        related_name="telefonos",
        primary_key=True,
    )
    telefono = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = "persona_telefonos"
        constraints = [
            models.UniqueConstraint(fields=["doc_persona", "telefono"], name="unique_persona_telefono"),
        ]


class PersonaCorreo(models.Model):
    doc_persona = models.ForeignKey(
        Persona,
        db_column="doc_persona",
        to_field="num_documento",
        on_delete=models.DO_NOTHING,
        related_name="correos",
        primary_key=True,
    )
    email = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = "persona_correo"
        constraints = [
            models.UniqueConstraint(fields=["doc_persona", "email"], name="unique_persona_correo"),
        ]


class Administrador(models.Model):
    numero_documento = models.OneToOneField(
        Persona,
        db_column="numero_documento",
        to_field="num_documento",
        on_delete=models.DO_NOTHING,
        related_name="administrador",
        primary_key=True,
    )
    rol = models.CharField(max_length=50)
    inicio_gestion = models.DateField()
    fin_gestion = models.DateField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "administrador"


class GuardiaSeguridad(models.Model):
    numero_documento = models.OneToOneField(
        Persona,
        db_column="numero_documento",
        to_field="num_documento",
        on_delete=models.DO_NOTHING,
        related_name="guardia_seguridad",
        primary_key=True,
    )
    empresa = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "guardia_seguridad"


class Residente(models.Model):
    numero_documento = models.OneToOneField(
        Persona,
        db_column="numero_documento",
        to_field="num_documento",
        on_delete=models.DO_NOTHING,
        related_name="residente",
        primary_key=True,
    )
    id_apartamento = models.SmallIntegerField(db_column="id_apartamento")

    class Meta:
        managed = False
        db_table = "residente"
