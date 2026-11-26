from django.db import transaction
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from infraestructura.models import Parqueadero
from vehiculos.models import Vehiculo

from .models import RegistroAcceso, Turno
from .serializers import (
    IngresoRequestSerializer,
    IngresoResponseSerializer,
    RegistroAccesoSerializer,
    TurnoSerializer,
)


class TurnoViewSet(viewsets.ModelViewSet):
    serializer_class = TurnoSerializer
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_queryset(self):
        queryset = Turno.objects.select_related("num_documento_guardia").all().order_by("-fecha_turno", "-id_turno")
        fecha_turno = self.request.query_params.get("fecha_turno")
        guardia = self.request.query_params.get("num_documento_guardia")

        if fecha_turno:
            queryset = queryset.filter(fecha_turno=fecha_turno)
        if guardia:
            queryset = queryset.filter(num_documento_guardia=guardia)

        return queryset


class RegistroAccesoViewSet(viewsets.ModelViewSet):
    serializer_class = RegistroAccesoSerializer
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_queryset(self):
        queryset = RegistroAcceso.objects.select_related("placa", "id_turno", "celda_asignada").all().order_by("-id_registro")
        placa = self.request.query_params.get("placa")
        id_turno = self.request.query_params.get("id_turno")
        fecha_entrada = self.request.query_params.get("fecha_entrada")
        en_parqueadero = self.request.query_params.get("en_parqueadero")

        if placa:
            queryset = queryset.filter(placa__placa__iexact=placa.strip())
        if id_turno:
            queryset = queryset.filter(id_turno=id_turno)
        if fecha_entrada:
            queryset = queryset.filter(fecha_entrada=fecha_entrada)
        if en_parqueadero and en_parqueadero.lower() == "true":
            queryset = queryset.filter(fecha_salida__isnull=True, hora_salida__isnull=True)

        return queryset

    @extend_schema(
        request=IngresoRequestSerializer,
        responses={201: IngresoResponseSerializer},
        summary="Registrar ingreso y asignar celda",
        description="Crea el registro de acceso, reserva una celda disponible y la marca como Ocupado.",
    )
    @action(detail=False, methods=["post"], url_path="ingreso")
    def ingreso(self, request):
        serializer = IngresoRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        placa = serializer.validated_data["placa"].strip().upper()
        id_turno = serializer.validated_data["id_turno"]

        vehiculo = Vehiculo.objects.filter(placa=placa).first()
        if vehiculo is None:
            raise ValidationError("No existe un vehículo con esa placa.")

        turno = Turno.objects.filter(pk=id_turno).first()
        if turno is None:
            raise ValidationError("No existe el turno indicado.")

        with transaction.atomic():
            celda = (
                Parqueadero.objects.select_for_update()
                .filter(estado__iexact="Disponible")
                .order_by("id_parqueadero")
                .first()
            )
            if celda is None:
                raise ValidationError("No hay celdas disponibles en el parqueadero.")

            registro = RegistroAcceso.objects.create(
                placa=vehiculo,
                id_turno=turno,
                fecha_entrada=timezone.localdate(),
                hora_entrada=timezone.localtime().time(),
                celda_asignada=celda,
            )
            celda.estado = "Ocupado"
            celda.save(update_fields=["estado"])

        respuesta = IngresoResponseSerializer(
            {
                "id_registro": registro.id_registro,
                "celda_asignada": celda.id_parqueadero,
                "mensaje": "Ingreso registrado y celda asignada correctamente.",
            }
        )
        return Response(respuesta.data, status=status.HTTP_201_CREATED)
