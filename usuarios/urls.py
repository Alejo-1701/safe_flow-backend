from rest_framework.routers import DefaultRouter

from .views import PerfilViewSet

router = DefaultRouter()
router.register("perfiles", PerfilViewSet)

urlpatterns = router.urls
