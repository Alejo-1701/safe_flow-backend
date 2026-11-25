from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PagoViewSet, RecaudoViewSet, TarifaViewSet

router = DefaultRouter()
router.register(r"tarifas", TarifaViewSet, basename="tarifa")
router.register(r"pagos", PagoViewSet, basename="pago")
router.register(r"recaudos", RecaudoViewSet, basename="recaudo")

urlpatterns = [
    path("", include(router.urls)),
]
