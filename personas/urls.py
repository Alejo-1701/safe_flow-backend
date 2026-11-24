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
router.register("roles", RolViewSet)
router.register("empresas", EmpresaVigilanciaViewSet)
router.register("personas", PersonaViewSet)
router.register("telefonos", PersonaTelefonoViewSet)
router.register("correos", PersonaCorreoViewSet)
router.register("administradores", AdministradorViewSet)
router.register("guardias", GuardiaSeguridadViewSet)
router.register("residentes", ResidenteViewSet)

urlpatterns = router.urls
