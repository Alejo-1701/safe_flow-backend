from rest_framework.routers import DefaultRouter

from .views import NotificacionEstadoViewSet, NotificacionViewSet

router = DefaultRouter()
router.register("notificaciones", NotificacionViewSet, basename="notificacion")
router.register("notificacion-estados", NotificacionEstadoViewSet, basename="notificacionestado")

urlpatterns = router.urls
