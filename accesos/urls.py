from rest_framework.routers import DefaultRouter
from .views import TurnoViewSet, RegistroAccesoViewSet

router = DefaultRouter()
router.register(r'turnos', TurnoViewSet, basename='turno')
router.register(r'registros', RegistroAccesoViewSet, basename='registro-acceso')

urlpatterns = router.urls