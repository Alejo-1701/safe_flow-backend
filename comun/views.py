from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import NotificacionEstadoSerializer, NotificacionSerializer
from .services import NotificacionEstadoService, NotificacionService


class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer

    def get_queryset(self):
        queryset = NotificacionService.listar().order_by("-fecha_creacion", "-id_notificacion")
        numero_documento = self.request.query_params.get("numero_documento")
        if numero_documento:
            queryset = queryset.filter(numero_documento=numero_documento.strip())
        return queryset

    def get_object(self):
        obj = NotificacionService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto = NotificacionService.crear(serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instancia = self.get_object()
        serializer = self.get_serializer(instancia, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto = NotificacionService.actualizar(instancia, serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        NotificacionService.eliminar(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificacionEstadoViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionEstadoSerializer

    def get_queryset(self):
        return NotificacionEstadoService.listar()

    def get_object(self):
        obj = NotificacionEstadoService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto = NotificacionEstadoService.crear(serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instancia = self.get_object()
        serializer = self.get_serializer(instancia, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto = NotificacionEstadoService.actualizar(instancia, serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        NotificacionEstadoService.eliminar(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)
