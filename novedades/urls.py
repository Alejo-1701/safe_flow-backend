from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IncidentesViewSet, SolicitudViewSet, NotificacionViewSet

router = DefaultRouter()
router.register(r'incidentes', IncidentesViewSet, basename='incidentes')
router.register(r'solicitudes', SolicitudViewSet, basename='solicitudes')
router.register(r'notificaciones', NotificacionViewSet, basename='notificaciones')

urlpatterns = [
    path('', include(router.urls)),
]