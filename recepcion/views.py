# recepcion/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Estadia, HuespedEstadia
from .serializers import EstadiaSerializer, HuespedEstadiaSerializer

class EstadiaViewSet(viewsets.ModelViewSet):
    """
    API para la gestión de Estadías (Asignación de Habitaciones a una Reserva).
    Aquí ocurre la validación de solapamiento de fechas y el cambio de estado de la habitación.
    """
    # Optimización: Cargamos la Reserva y la Habitación en una sola consulta
    queryset = Estadia.objects.select_related('reserva', 'habitacion', 'habitacion__tipo').all()
    serializer_class = EstadiaSerializer
    permission_classes = [IsAuthenticated]

class HuespedEstadiaViewSet(viewsets.ModelViewSet):
    """
    API para registrar los Ocupantes de una Habitación/Estadía.
    Se usa en el proceso de Check-In para registrar a todos los huéspedes.
    """
    queryset = HuespedEstadia.objects.select_related('estadia', 'huesped').all()
    serializer_class = HuespedEstadiaSerializer
    permission_classes = [IsAuthenticated]