from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AutorizacionVisitaViewSet

router = DefaultRouter()
router.root_view_name = "visitas-api-root"
router.register(r"autorizaciones", AutorizacionVisitaViewSet, basename="autorizacionvisita")

urlpatterns = [
    path("", include(router.urls)),
]
