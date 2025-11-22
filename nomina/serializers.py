# nomina/serializers.py
from rest_framework import serializers
from .models import ConceptoNomina, Liquidacion, DetalleLiquidacion

# --- 1. Serializer para el Detalle (Líneas del Recibo) ---
class DetalleLiquidacionSerializer(serializers.ModelSerializer):
    concepto_nombre = serializers.CharField(source='concepto.nombre', read_only=True)
    id = serializers.UUIDField(read_only=True)
    
    class Meta:
        model = DetalleLiquidacion
        fields = ['id', 'concepto', 'concepto_nombre', 'monto', 'cantidad']
        read_only_fields = ['id', 'liquidacion']

# --- 2. Serializer para la Liquidación Principal ---
class LiquidacionSerializer(serializers.ModelSerializer):
    detalles = DetalleLiquidacionSerializer(many=True, read_only=True)
    empleado_nombre_completo = serializers.CharField(source='empleado.__str__', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Liquidacion
        fields = [
            'id', 'empleado', 'empleado_nombre_completo', 'fecha_inicio_periodo', 
            'fecha_fin_periodo', 'monto_bruto', 'monto_neto', 'estado', 'estado_display', 
            'detalles', 'created_at'
        ]
        read_only_fields = ['monto_bruto', 'monto_neto', 'created_at'] # Se calculan, no se escriben