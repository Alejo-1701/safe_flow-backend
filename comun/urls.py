from rest_framework.routers import DefaultRouter

from .views import NotificacionEstadoViewSet, NotificacionViewSet

router = DefaultRouter()
router.register("notificaciones", NotificacionViewSet)
router.register("notificacion-estados", NotificacionEstadoViewSet)

urlpatterns = router.urls
