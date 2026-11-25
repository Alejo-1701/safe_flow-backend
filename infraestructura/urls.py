from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApartamentoViewSet, AsambleaCopropietariosViewSet, ParqueaderoViewSet

router = DefaultRouter()
router.register(r'apartamentos', ApartamentoViewSet, basename='apartamento')
router.register(r'parqueaderos', ParqueaderoViewSet, basename='parqueadero')
router.register(r'asambleas', AsambleaCopropietariosViewSet, basename='asambleacopropietarios')

urlpatterns = [
    path('', include(router.urls)),
]