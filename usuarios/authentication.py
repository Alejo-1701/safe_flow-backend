from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework_simplejwt.authentication import AuthenticationFailed, JWTAuthentication

from .models import Perfil


class PerfilJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    """Documenta el Bearer JWT de Perfil en el esquema OpenAPI."""

    target_class = "usuarios.authentication.PerfilJWTAuthentication"
    name = "bearerAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }


class PerfilJWTAuthentication(JWTAuthentication):
    """Resuelve el usuario autenticado desde un Perfil de SafeFlow, no desde auth.User."""

    def get_user(self, validated_token):
        user_id = validated_token.get("user_id")
        if not user_id:
            raise AuthenticationFailed("El token no contiene user_id.")

        try:
            perfil = Perfil.objects.select_related("doc_persona__id_rol").get(
                doc_persona_id=user_id
            )
        except Perfil.DoesNotExist as exc:
            raise AuthenticationFailed("Perfil no encontrado para el token.") from exc

        if perfil.estado_perfil is not True:
            raise AuthenticationFailed("El perfil está inactivo.")

        perfil.is_authenticated = True
        perfil.is_active = True
        return perfil
