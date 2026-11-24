from django.http import Http404
from rest_framework import viewsets

from .serializers import (
    AdministradorSerializer,
    EmpresaVigilanciaSerializer,
    GuardiaSeguridadSerializer,
    PersonaCorreoSerializer,
    PersonaSerializer,
    PersonaTelefonoSerializer,
    ResidenteSerializer,
    RolSerializer,
)
from .services import (
    AdministradorService,
    EmpresaVigilanciaService,
    GuardiaSeguridadService,
    PersonaCorreoService,
    PersonaService,
    PersonaTelefonoService,
    ResidenteService,
    RolService,
)


class RolViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RolSerializer

    def get_queryset(self):
        return RolService.listar()

    def get_object(self):
        obj = RolService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj


class EmpresaVigilanciaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EmpresaVigilanciaSerializer

    def get_queryset(self):
        return EmpresaVigilanciaService.listar()

    def get_object(self):
        obj = EmpresaVigilanciaService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj


class PersonaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PersonaSerializer

    def get_queryset(self):
        return PersonaService.listar()

    def get_object(self):
        obj = PersonaService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj


class PersonaTelefonoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PersonaTelefonoSerializer

    def get_queryset(self):
        return PersonaTelefonoService.listar()

    def get_object(self):
        obj = PersonaTelefonoService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj


class PersonaCorreoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PersonaCorreoSerializer

    def get_queryset(self):
        return PersonaCorreoService.listar()

    def get_object(self):
        obj = PersonaCorreoService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj


class AdministradorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AdministradorSerializer

    def get_queryset(self):
        return AdministradorService.listar()

    def get_object(self):
        obj = AdministradorService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj


class GuardiaSeguridadViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GuardiaSeguridadSerializer

    def get_queryset(self):
        return GuardiaSeguridadService.listar()

    def get_object(self):
        obj = GuardiaSeguridadService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj


class ResidenteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ResidenteSerializer

    def get_queryset(self):
        return ResidenteService.listar()

    def get_object(self):
        obj = ResidenteService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj
