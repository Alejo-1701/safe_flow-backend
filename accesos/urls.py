from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TurnoViewSet, RegistroAccesoViewSet

router = DefaultRouter()
router.register(r'turnos', TurnoViewSet, basename='turno')
router.register(r'registros', RegistroAccesoViewSet, basename='registro-acceso')

urlpatterns = [
    path('', include(router.urls)),
]