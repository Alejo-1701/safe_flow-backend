from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApartamentoViewSet, ParqueaderoViewSet

router = DefaultRouter()
router.register(r'apartamentos', ApartamentoViewSet, basename='apartamento')
router.register(r'parqueaderos', ParqueaderoViewSet, basename='parqueadero')

urlpatterns = [
    path('', include(router.urls)),
]