from django.contrib.auth.hashers import check_password, identify_hasher
from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Perfil
from .serializers import LoginRequestSerializer, LoginResponseSerializer, PerfilSerializer
from .services import PerfilService


class LoginView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def _password_valida(contrasenia: str, almacenada: str) -> bool:
        try:
            identify_hasher(almacenada)
        except (ValueError, TypeError):
            return contrasenia == almacenada
        return check_password(contrasenia, almacenada)

    @extend_schema(
        request=LoginRequestSerializer,
        responses={
            200: LoginResponseSerializer,
            400: None,
            401: None,
            403: None,
        },
        summary="Iniciar sesión",
        description="Valida Perfil, emite tokens JWT y retorna datos básicos del usuario.",
    )
    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        num_documento = serializer.validated_data["num_documento"].strip()
        contrasenia = serializer.validated_data["contrasenia"]

        perfil = Perfil.objects.select_related("doc_persona__id_rol").filter(
            doc_persona_id=num_documento
        ).first()
        if perfil is None:
            return Response(
                {"detail": "Credenciales inválidas."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not self._password_valida(contrasenia, perfil.contrasenia or ""):
            return Response(
                {"detail": "Credenciales inválidas."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if perfil.estado_perfil is not True:
            return Response(
                {"detail": "El perfil está inactivo."},
                status=status.HTTP_403_FORBIDDEN,
            )

        persona = perfil.doc_persona
        nombre_completo = " ".join(
            parte
            for parte in [
                persona.primer_nombre,
                persona.segundo_nombre,
                persona.primer_apellido,
                persona.segundo_apellido,
            ]
            if parte
        )
        rol = persona.id_rol.nombre_rol if persona.id_rol_id else ""

        refresh = RefreshToken()
        refresh["user_id"] = str(perfil.doc_persona_id)
        refresh["num_documento"] = perfil.doc_persona_id
        refresh["rol"] = rol

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "num_documento": perfil.doc_persona_id,
                "nombre_completo": nombre_completo,
                "rol": rol,
            },
            status=status.HTTP_200_OK,
        )


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
