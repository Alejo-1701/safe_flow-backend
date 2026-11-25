from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import PerfilSerializer
from .services import PerfilService


class PerfilViewSet(viewsets.ModelViewSet):
    serializer_class = PerfilSerializer

    def get_queryset(self):
        return PerfilService.listar()

    def get_object(self):
        obj = PerfilService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto = PerfilService.crear(serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instancia = self.get_object()
        serializer = self.get_serializer(instancia, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto = PerfilService.actualizar(instancia, serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        PerfilService.eliminar(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)
