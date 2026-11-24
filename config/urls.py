from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Documentación interactiva Swagger / OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Endpoints de los módulos de Thomas
    path('api/', include('vehiculos.urls')),
    path('api/infraestructura/', include('infraestructura.urls')),

    # Endpoints de los módulos del equipo
    path('api/comun/', include('comun.urls')),
    path('api/usuarios/', include('usuarios.urls')),
    path('api/personas/', include('personas.urls')),
]