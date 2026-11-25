from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/', include('vehiculos.urls')),
    path('api/infraestructura/', include('infraestructura.urls')),
    path('api/comun/', include('comun.urls')),
    path('api/usuarios/', include('usuarios.urls')),
    path('api/personas/', include('personas.urls')),
    path('api/accesos/', include('accesos.urls')),
    path('api/visitas/', include('visitas.urls')),
    path('api/financiero/', include('financiero.urls')),
    path('api/novedades/', include('novedades.urls')),
]