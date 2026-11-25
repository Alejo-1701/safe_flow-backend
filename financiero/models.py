from django.db import models

class AsambleaCopropietarios(models.Model):
    id_asamblea = models.SmallAutoField(primary_key=True)
    numero_acta = models.CharField(max_length=20)
    fecha_reunion = models.DateField()
    art_referencia = models.CharField(max_length=30)
    des_acuerdo = models.TextField()

    class Meta:
        db_table = 'asamblea_copropietarios'


class Tarifa(models.Model):
    id_tarifa = models.SmallAutoField(primary_key=True)
    tipo_vehiculo = models.CharField(max_length=20)  # Ej: Carro, Moto
    valor_minuto = models.DecimalField(max_digits=10, decimal_places=2)
    id_asamblea = models.ForeignKey(
        AsambleaCopropietarios,
        on_delete=models.RESTRICT,
        db_column='id_asamblea'
    )

    class Meta:
        db_table = 'tarifa'


class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    metodo_pago = models.CharField(max_length=30)  # Efectivo, Transferencia
    fecha_pago = models.DateField(auto_now_add=True)
    hora_pago = models.TimeField(auto_now_add=True)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)
    id_registro = models.OneToOneField(
        'accesos.RegistroAcceso',
        on_delete=models.RESTRICT,
        db_column='id_registro'
    )
    id_turno = models.ForeignKey(
        'accesos.Turno',
        on_delete=models.RESTRICT,
        db_column='id_turno'
    )

    class Meta:
        db_table = 'pago'


class Recaudo(models.Model):
    numero_factura = models.AutoField(primary_key=True)
    id_pago = models.OneToOneField(
        Pago,
        on_delete=models.RESTRICT,
        db_column='id_pago'
    )
    id_tarifa = models.ForeignKey(
        Tarifa,
        on_delete=models.RESTRICT,
        db_column='id_tarifa'
    )
    id_confirmacion = models.CharField(max_length=50, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    total_pagado = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'recaudo'