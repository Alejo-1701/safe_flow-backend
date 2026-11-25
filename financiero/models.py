from django.db import models


class Tarifa(models.Model):
    id_tarifa = models.SmallAutoField(primary_key=True, db_column="id_tarifa")
    tipo_vehiculo = models.CharField(max_length=20)
    valor_minuto = models.DecimalField(max_digits=12, decimal_places=2)
    id_asamblea = models.ForeignKey(
        "infraestructura.AsambleaCopropietarios",
        db_column="id_asamblea",
        to_field="id_asamblea",
        on_delete=models.DO_NOTHING,
        related_name="tarifas",
    )

    class Meta:
        managed = False
        db_table = "tarifa"


class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True, db_column="id_pago")
    metodo_pago = models.CharField(max_length=20)
    fecha_caja = models.DateField()
    hora_caja = models.TimeField()
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)
    id_registro = models.ForeignKey(
        "accesos.RegistroAcceso",
        db_column="id_registro",
        to_field="id_registro",
        on_delete=models.DO_NOTHING,
        related_name="pagos",
    )
    id_turno = models.ForeignKey(
        "accesos.Turno",
        db_column="id_turno",
        to_field="id_turno",
        on_delete=models.DO_NOTHING,
        related_name="pagos_turno",
    )

    class Meta:
        managed = False
        db_table = "pago"


class Recaudo(models.Model):
    numero_factura = models.AutoField(primary_key=True, db_column="numero_factura")
    id_pago = models.ForeignKey(
        "financiero.Pago",
        db_column="id_pago",
        to_field="id_pago",
        on_delete=models.DO_NOTHING,
        related_name="recaudos",
    )
    id_tarifa = models.ForeignKey(
        "financiero.Tarifa",
        db_column="id_tarifa",
        to_field="id_tarifa",
        on_delete=models.DO_NOTHING,
        related_name="recaudos",
    )
    id_confirmacion = models.CharField(max_length=50)
    sub_total = models.DecimalField(max_digits=12, decimal_places=2)
    total_pagado = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = False
        db_table = "recaudo"
