from rest_framework.routers import DefaultRouter
from .views import AutorizacionVisitaViewSet

router = DefaultRouter()
router.register(r'autorizaciones', AutorizacionVisitaViewSet, basename='autorizacion-visita')

urlpatterns = router.urls