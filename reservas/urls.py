# reservas/urls.py
from rest_framework.routers import DefaultRouter
from .views import ReservaViewSet

router = DefaultRouter()

# Registra el ViewSet. La URL base será 'api/reservas/'
router.register(r'', ReservaViewSet) 

urlpatterns = router.urls