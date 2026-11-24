from django.http import Http404
from rest_framework import viewsets

from .serializers import PerfilSerializer
from .services import PerfilService


class PerfilViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PerfilSerializer

    def get_queryset(self):
        return PerfilService.listar()

    def get_object(self):
        obj = PerfilService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj
