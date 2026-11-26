from django.http import Http404
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import PersonaCorreo, PersonaTelefono
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


class RolViewSet(viewsets.ModelViewSet):
    serializer_class = RolSerializer

    def get_queryset(self):
        return RolService.listar()

    def get_object(self):
        obj = RolService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto = RolService.crear(serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instancia = self.get_object()
        serializer = self.get_serializer(instancia, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto = RolService.actualizar(instancia, serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        RolService.eliminar(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmpresaVigilanciaViewSet(viewsets.ModelViewSet):
    serializer_class = EmpresaVigilanciaSerializer

    def get_queryset(self):
        return EmpresaVigilanciaService.listar()

    def get_object(self):
        obj = EmpresaVigilanciaService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto = EmpresaVigilanciaService.crear(serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instancia = self.get_object()
        serializer = self.get_serializer(instancia, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto = EmpresaVigilanciaService.actualizar(instancia, serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        EmpresaVigilanciaService.eliminar(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonaViewSet(viewsets.ModelViewSet):
    serializer_class = PersonaSerializer

    def get_queryset(self):
        return PersonaService.listar()

    def get_object(self):
        obj = PersonaService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto = PersonaService.crear(serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instancia = self.get_object()
        serializer = self.get_serializer(instancia, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto = PersonaService.actualizar(instancia, serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        PersonaService.eliminar(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonaTelefonoViewSet(viewsets.ModelViewSet):
    serializer_class = PersonaTelefonoSerializer

    def get_queryset(self):
        queryset = PersonaTelefonoService.listar()
        doc_persona = self.request.query_params.get("doc_persona")
        if doc_persona:
            queryset = queryset.filter(doc_persona=doc_persona.strip())
        return queryset

    def get_object(self):
        obj = PersonaTelefonoService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto = PersonaTelefonoService.crear(serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instancia = self.get_object()
        serializer = self.get_serializer(instancia, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto = PersonaTelefonoService.actualizar(instancia, serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        PersonaTelefonoService.eliminar(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        parameters=[
            OpenApiParameter(name="doc_persona", required=True, type=str),
            OpenApiParameter(name="telefono", required=True, type=str),
        ],
        request=None,
        responses={204: None, 404: None},
        summary="Eliminar teléfono exacto",
    )
    @action(detail=False, methods=["delete"], url_path="eliminar")
    def eliminar(self, request):
        doc_persona = request.query_params.get("doc_persona")
        telefono = request.query_params.get("telefono")
        if not doc_persona or not telefono:
            raise ValidationError("Se requieren los parámetros doc_persona y telefono.")

        eliminados, _ = PersonaTelefono.objects.filter(
            doc_persona=doc_persona.strip(),
            telefono=telefono.strip(),
        ).delete()
        if eliminados == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonaCorreoViewSet(viewsets.ModelViewSet):
    serializer_class = PersonaCorreoSerializer

    def get_queryset(self):
        queryset = PersonaCorreoService.listar()
        doc_persona = self.request.query_params.get("doc_persona")
        if doc_persona:
            queryset = queryset.filter(doc_persona=doc_persona.strip())
        return queryset

    def get_object(self):
        obj = PersonaCorreoService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto = PersonaCorreoService.crear(serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instancia = self.get_object()
        serializer = self.get_serializer(instancia, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto = PersonaCorreoService.actualizar(instancia, serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        PersonaCorreoService.eliminar(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        parameters=[
            OpenApiParameter(name="doc_persona", required=True, type=str),
            OpenApiParameter(name="email", required=True, type=str),
        ],
        request=None,
        responses={204: None, 404: None},
        summary="Eliminar correo exacto",
    )
    @action(detail=False, methods=["delete"], url_path="eliminar")
    def eliminar(self, request):
        doc_persona = request.query_params.get("doc_persona")
        email = request.query_params.get("email")
        if not doc_persona or not email:
            raise ValidationError("Se requieren los parámetros doc_persona y email.")

        eliminados, _ = PersonaCorreo.objects.filter(
            doc_persona=doc_persona.strip(),
            email=email.strip(),
        ).delete()
        if eliminados == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdministradorViewSet(viewsets.ModelViewSet):
    serializer_class = AdministradorSerializer

    def get_queryset(self):
        return AdministradorService.listar()

    def get_object(self):
        obj = AdministradorService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto = AdministradorService.crear(serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instancia = self.get_object()
        serializer = self.get_serializer(instancia, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto = AdministradorService.actualizar(instancia, serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        AdministradorService.eliminar(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


class GuardiaSeguridadViewSet(viewsets.ModelViewSet):
    serializer_class = GuardiaSeguridadSerializer

    def get_queryset(self):
        return GuardiaSeguridadService.listar()

    def get_object(self):
        obj = GuardiaSeguridadService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto = GuardiaSeguridadService.crear(serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instancia = self.get_object()
        serializer = self.get_serializer(instancia, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto = GuardiaSeguridadService.actualizar(instancia, serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        GuardiaSeguridadService.eliminar(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResidenteViewSet(viewsets.ModelViewSet):
    serializer_class = ResidenteSerializer

    def get_queryset(self):
        return ResidenteService.listar()

    def get_object(self):
        obj = ResidenteService.obtener(self.kwargs["pk"])
        if obj is None:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        objeto = ResidenteService.crear(serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instancia = self.get_object()
        serializer = self.get_serializer(instancia, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        objeto = ResidenteService.actualizar(instancia, serializer.validated_data)
        return Response(self.get_serializer(objeto).data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        ResidenteService.eliminar(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)
