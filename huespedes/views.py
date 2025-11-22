# huespedes/views.py
from rest_framework import viewsets
from .models import Huesped
from .serializers import HuespedSerializer
from rest_framework.permissions import IsAuthenticated # ¡Añadimos seguridad!

class HuespedViewSet(viewsets.ModelViewSet):
    """
    API para la gestión de huéspedes.
    Permite crear, ver, actualizar y eliminar perfiles de personas.
    """
    queryset = Huesped.objects.all()
    serializer_class = HuespedSerializer
    
    # 🚨 Seguridad: Solo usuarios autenticados con un token JWT pueden usar este ViewSet.
    permission_classes = [IsAuthenticated]