# reservas/views.py
from rest_framework import viewsets
from .models import Reserva
from .serializers import ReservaSerializer
from rest_framework.permissions import IsAuthenticated

class ReservaViewSet(viewsets.ModelViewSet):
    """
    API para la gestión completa de Reservas.
    Utilizado por Recepción y Gerencia.
    """
    
    # 🚨 Optimización: Usamos select_related para cargar los datos 
    # de Huésped y Habitación en una sola consulta a la BD.
    queryset = Reserva.objects.select_related(
        'huesped_titular', 
        'habitacion', 
        'habitacion__tipo'
    ).all()
    
    serializer_class = ReservaSerializer
    
    # 🚨 Seguridad: Solo usuarios autenticados pueden manejar reservas
    permission_classes = [IsAuthenticated]