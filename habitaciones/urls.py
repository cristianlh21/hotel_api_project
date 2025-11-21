# habitaciones/urls.py
from rest_framework.routers import DefaultRouter
from .views import TipoHabitacionViewSet, HabitacionViewSet

# Inicializa el router
router = DefaultRouter()

# Registra los ViewSets. El primer argumento es la URL base
router.register(r'tipos', TipoHabitacionViewSet) # URL: api/habitaciones/tipos/
router.register(r'', HabitacionViewSet) # URL: api/habitaciones/

urlpatterns = router.urls