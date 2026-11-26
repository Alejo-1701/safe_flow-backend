from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import LoginView, PerfilViewSet

router = DefaultRouter()
router.register("perfiles", PerfilViewSet, basename="perfil")

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
] + router.urls
