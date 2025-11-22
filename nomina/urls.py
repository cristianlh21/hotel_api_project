# nomina/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ConceptoNominaViewSet, LiquidacionViewSet

router = DefaultRouter()

router.register(r'conceptos', ConceptoNominaViewSet)
# La ruta 'calcular' se añade automáticamente a /liquidaciones/calcular/
router.register(r'liquidaciones', LiquidacionViewSet) 

urlpatterns = [
    path('', include(router.urls)),
]