from rest_framework import viewsets

from .models import (
    Administrador,
    EmpresaVigilancia,
    GuardiaSeguridad,
    Persona,
    PersonaCorreo,
    PersonaTelefono,
    Residente,
    Rol,
)
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


class RolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer


class EmpresaVigilanciaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EmpresaVigilancia.objects.all()
    serializer_class = EmpresaVigilanciaSerializer


class PersonaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class PersonaTelefonoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PersonaTelefono.objects.all()
    serializer_class = PersonaTelefonoSerializer


class PersonaCorreoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PersonaCorreo.objects.all()
    serializer_class = PersonaCorreoSerializer


class AdministradorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer


class GuardiaSeguridadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GuardiaSeguridad.objects.all()
    serializer_class = GuardiaSeguridadSerializer


class ResidenteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Residente.objects.all()
    serializer_class = ResidenteSerializer
