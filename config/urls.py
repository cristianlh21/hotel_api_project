# config/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView # ¡Importar las vistas!

urlpatterns = [
    # 1. Rutas del Panel de Administración
    path('admin/', admin.site.urls),
    
    # 2. Rutas para obtener y refrescar tokens JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 3. Rutas para la documentación (¡Nuevas!)
    # Genera el archivo OpenAPI (YAML/JSON)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'), 
    # Muestra la interfaz gráfica interactiva (Swagger UI)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # 4. Rutas de nuestras Apps modulares (Vacías por ahora)
    # path('api/users/', include('users.urls')),
]