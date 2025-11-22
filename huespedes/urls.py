# huespedes/urls.py
from rest_framework.routers import DefaultRouter
from .views import HuespedViewSet

router = DefaultRouter()

# Registra el ViewSet. La URL base será 'api/huespedes/'
router.register(r'', HuespedViewSet) 

urlpatterns = router.urls