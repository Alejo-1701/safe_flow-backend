from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AsambleaViewSet, TarifaViewSet, PagoViewSet, RecaudoViewSet

router = DefaultRouter()
router.register(r'asambleas', AsambleaViewSet, basename='asambleas')
router.register(r'tarifas', TarifaViewSet, basename='tarifas')
router.register(r'pagos', PagoViewSet, basename='pagos')
router.register(r'recaudos', RecaudoViewSet, basename='recaudos')

urlpatterns = [
    path('', include(router.urls)),
]