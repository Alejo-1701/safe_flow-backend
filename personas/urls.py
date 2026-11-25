from rest_framework.routers import DefaultRouter

from .views import (
    AdministradorViewSet,
    EmpresaVigilanciaViewSet,
    GuardiaSeguridadViewSet,
    PersonaCorreoViewSet,
    PersonaTelefonoViewSet,
    PersonaViewSet,
    ResidenteViewSet,
    RolViewSet,
)

router = DefaultRouter()
router.root_view_name = "personas-api-root"
router.register("roles", RolViewSet, basename="rol")
router.register("empresas", EmpresaVigilanciaViewSet, basename="empresavigilancia")
router.register("personas", PersonaViewSet, basename="persona")
router.register("telefonos", PersonaTelefonoViewSet, basename="personatelefono")
router.register("correos", PersonaCorreoViewSet, basename="personacorreo")
router.register("administradores", AdministradorViewSet, basename="administrador")
router.register("guardias", GuardiaSeguridadViewSet, basename="guardiasseguridad")
router.register("residentes", ResidenteViewSet, basename="residente")

urlpatterns = router.urls
