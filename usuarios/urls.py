from rest_framework.routers import DefaultRouter

from .views import PerfilViewSet

router = DefaultRouter()
router.root_view_name = "usuarios-api-root"
router.register("perfiles", PerfilViewSet, basename="perfil")

urlpatterns = router.urls
