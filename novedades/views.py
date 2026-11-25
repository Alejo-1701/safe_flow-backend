from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Incidentes, Solicitud, Notificacion
from .serializers import IncidentesSerializer, SolicitudSerializer, NotificacionSerializer

class IncidentesViewSet(viewsets.ModelViewSet):
    queryset = Incidentes.objects.all().order_by('-fecha_incidente')
    serializer_class = IncidentesSerializer

class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all().order_by('-fecha_solicitud')
    serializer_class = SolicitudSerializer

    # PATCH /api/solicitudes/{id}/cambiar-estado/
    @action(detail=True, methods=['patch'], url_path='cambiar-estado')
    def cambiar_estado(self, request, pk=None):
        solicitud = self.get_object()
        nuevo_estado = request.data.get('estado_solicitud')
        if nuevo_estado not in ['Pendiente', 'Aprobada', 'Rechazada']:
            return Response({"error": "Estado no válido"}, status=status.HTTP_400_BAD_REQUEST)
        solicitud.estado_solicitud = nuevo_estado
        solicitud.save()
        return Response(self.get_serializer(solicitud).data)

class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer

    # GET /api/notificaciones/usuario/?doc=12345
    @action(detail=False, methods=['get'], url_path='usuario')
    def por_usuario(self, request):
        doc = request.query_params.get('doc')
        notifs = self.queryset.filter(numero_documento=doc)
        return Response(self.get_serializer(notifs, many=True).data)