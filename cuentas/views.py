# cuentas/views.py
from rest_framework import viewsets
from .models import Cuenta, Transaccion
from .serializers import CuentaSerializer, TransaccionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

class CuentaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API para ver los Folios de Huéspedes.
    ReadOnly: Las cuentas se crean automáticamente con el Check-In, no manualmente.
    """
    queryset = Cuenta.objects.all().select_related('reserva', 'reserva__habitacion')
    serializer_class = CuentaSerializer
    permission_classes = [IsAuthenticated]
    
class TransaccionViewSet(viewsets.ModelViewSet):
    """
    API para la creación de Cargos y Pagos en los Folios activos.
    """
    queryset = Transaccion.objects.all().select_related('cuenta')
    serializer_class = TransaccionSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """Validación extra antes de guardar la transacción."""
        cuenta = serializer.validated_data.get('cuenta')
        
        # Opcional: Impedir transacciones en cuentas ya pagadas o cerradas
        if cuenta.estado == 'PAG':
            raise ValidationError(
                {"cuenta": "No se pueden añadir transacciones a una cuenta ya pagada."}
            )
            
        serializer.save()