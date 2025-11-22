# habitaciones/views.py
from rest_framework import viewsets
from .models import TipoHabitacion, Habitacion
from .serializers import TipoHabitacionSerializer, HabitacionSerializer
from rest_framework.decorators import action # Importar la función action
from rest_framework.response import Response
from reservas.models import Reserva # Necesario para la lógica de conflicto

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
    
    @action(detail=False, methods=['GET'], url_path='disponibles')
    def get_habitaciones_disponibles(self, request):
        """
        Endpoint que devuelve solo las habitaciones disponibles para un rango de fechas.
        Ejemplo de llamada: /api/habitaciones/disponibles/?checkin=YYYY-MM-DD&checkout=YYYY-MM-DD
        """
        
        # 1. Capturar fechas de los parámetros de URL
        checkin = request.query_params.get('checkin')
        checkout = request.query_params.get('checkout')
        
        if not checkin or not checkout:
             return Response({"error": "Debe proporcionar checkin y checkout."}, status=400)
        
        # 2. Identificar habitaciones CONFLICTIVAS (Reservadas o en Mantenimiento)
        
        # Habitaciones en Mantenimiento (Estado de Servicio 'M')
        mantenimiento_ids = Habitacion.objects.filter(estado_servicio='M').values_list('id', flat=True)
        
        # Habitaciones con Reservas Confirmadas/Activas que se solapen
        conflicto_ids = Reserva.objects.filter(
            estado__in=['CONF', 'CI']
        ).filter(
            fecha_checkin__lt=checkout, 
            fecha_checkout__gt=checkin
        ).values_list('habitacion_id', flat=True)
        
        # 3. Combinar IDs conflictivos y buscar todas las habitaciones que NO estén en esa lista
        
        # Concatenamos los IDs de conflicto y eliminamos duplicados
        ids_a_excluir = set(list(mantenimiento_ids) + list(conflicto_ids))
        
        # 4. Obtener las habitaciones disponibles
        disponibles = Habitacion.objects.exclude(id__in=ids_a_excluir).filter(
            # Opcional: solo mostrar habitaciones que no estén Ocupadas por si acaso
            estado_ocupacion__in=['L', 'R']
        )
        
        # 5. Serializar y devolver
        serializer = self.get_serializer(disponibles, many=True)
        return Response(serializer.data)

    # Puedes anular métodos aquí para agregar lógica de negocio (ej. permisos).
    # def create(self, request, *args, **kwargs):
    #    # Lógica personalizada antes de crear...
    #    pass