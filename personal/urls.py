# personal/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import DepartamentoViewSet, PuestoViewSet, EmpleadoViewSet

router = DefaultRouter()

router.register(r'departamentos', DepartamentoViewSet)
router.register(r'puestos', PuestoViewSet)
router.register(r'empleados', EmpleadoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]