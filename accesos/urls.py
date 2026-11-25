from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RegistroAccesoViewSet, TurnoViewSet

router = DefaultRouter()
router.root_view_name = "accesos-api-root"
router.register(r"turnos", TurnoViewSet, basename="turno")
router.register(r"registros-acceso", RegistroAccesoViewSet, basename="registroacceso")

urlpatterns = [
    path("", include(router.urls)),
]
