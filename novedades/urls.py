from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IncidenteViewSet, SolicitudViewSet

router = DefaultRouter()
router.register(r"incidentes", IncidenteViewSet, basename="incidente")
router.register(r"solicitudes", SolicitudViewSet, basename="solicitud")

urlpatterns = [
    path("", include(router.urls)),
]
