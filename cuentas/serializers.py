# cuentas/serializers.py
from rest_framework import serializers
from .models import Cuenta, Transaccion

# --- 1. SERIALIZER DE MOVIMIENTO (Transaccion) ---
class TransaccionSerializer(serializers.ModelSerializer):
    # Campo legible para el tipo (ej: 'CARGO' -> 'Cargo (Consumo/Tarifa)')
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Transaccion
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

# --- 2. SERIALIZER DE CUENTA (FOLIO) ---
class CuentaSerializer(serializers.ModelSerializer):
    # ANIDAMIENTO: Muestra todas las transacciones dentro de la cuenta
    transacciones = TransaccionSerializer(many=True, read_only=True)
    
    # LÓGICA DE NEGOCIO: Calculamos el saldo actual de la cuenta
    saldo_actual = serializers.SerializerMethodField()
    
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Cuenta
        # Exponemos la reserva asociada para saber a qué estadía pertenece
        fields = [
            'id', 'reserva', 'estado', 'estado_display', 
            'transacciones', 'saldo_actual', 'created_at'
        ]
        read_only_fields = ('reserva', 'created_at', 'updated_at')
        
    def get_saldo_actual(self, obj):
        """
        Calcula el saldo: Suma de CARGOS - Suma de PAGOS.
        """
        cargos = obj.transacciones.filter(tipo='CARGO').aggregate(
            total=models.Sum('monto')
        )['total'] or 0
        
        pagos = obj.transacciones.filter(tipo='PAGO').aggregate(
            total=models.Sum('monto')
        )['total'] or 0
        
        return cargos - pagos