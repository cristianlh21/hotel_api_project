# recepcion/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import EstadiaViewSet, HuespedEstadiaViewSet

router = DefaultRouter()

# 1. Ruta para asignar habitaciones (Ej: /api/recepcion/estadias/)
router.register(r'estadias', EstadiaViewSet) 
# 2. Ruta para registrar ocupantes (Ej: /api/recepcion/ocupantes/)
router.register(r'ocupantes', HuespedEstadiaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]