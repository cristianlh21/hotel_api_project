# habitaciones/views.py
from rest_framework import viewsets
from .models import TipoHabitacion, Habitacion
from .serializers import TipoHabitacionSerializer, HabitacionSerializer

# 1. ViewSet para TipoHabitacion
class TipoHabitacionViewSet(viewsets.ModelViewSet):
    """
    Permite ver, crear, actualizar y eliminar Tipos de Habitación.
    Ideal para el personal de administración.
    """
    queryset = TipoHabitacion.objects.all()
    serializer_class = TipoHabitacionSerializer

# 2. ViewSet para Habitacion
class HabitacionViewSet(viewsets.ModelViewSet):
    """
    Permite ver, crear y actualizar el estado de las Habitaciones.
    Usado por Recepción y Gobernanza.
    """
    queryset = Habitacion.objects.all()
    serializer_class = HabitacionSerializer

    # Puedes anular métodos aquí para agregar lógica de negocio (ej. permisos).
    # def create(self, request, *args, **kwargs):
    #    # Lógica personalizada antes de crear...
    #    pass