from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Incidente, Solicitud
from .serializers import (
    CambiarEstadoRequestSerializer,
    IncidenteSerializer,
    SolicitudSerializer,
)


class IncidenteViewSet(viewsets.ModelViewSet):
    queryset = Incidente.objects.all().order_by("id_incidente")
    serializer_class = IncidenteSerializer
    http_method_names = ["get", "post", "head", "options"]


class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all().order_by("id_solicitud")
    serializer_class = SolicitudSerializer
    http_method_names = ["get", "post", "patch", "head", "options"]

    @extend_schema(
        request=CambiarEstadoRequestSerializer,
        responses={200: SolicitudSerializer},
        summary="Cambiar estado de solicitud",
        description="Actualiza únicamente el campo estado_solicitud.",
    )
    @action(detail=True, methods=["patch"], url_path="cambiar-estado")
    def cambiar_estado(self, request, pk=None):
        instancia = self.get_object()
        serializer = CambiarEstadoRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instancia.estado_solicitud = serializer.validated_data["estado_solicitud"]
        instancia.save(update_fields=["estado_solicitud"])

        return Response(
            SolicitudSerializer(instancia).data,
            status=status.HTTP_200_OK,
        )
