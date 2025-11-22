# cuentas/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CuentaViewSet, TransaccionViewSet

router = DefaultRouter()

# 1. Ruta para los Folios (Cuentas)
router.register(r'cuentas', CuentaViewSet) 
# 2. Ruta para los Movimientos (Cargos/Pagos)
router.register(r'transacciones', TransaccionViewSet)

urlpatterns = [
    path('', include(router.urls)), # Incluimos ambas rutas
]