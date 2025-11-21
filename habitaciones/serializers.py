# habitaciones/serializers.py
from rest_framework import serializers
from .models import TipoHabitacion, Habitacion

# 1. Serializer para TipoHabitacion
class TipoHabitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoHabitacion
        # __all__ incluye todos los campos del modelo
        fields = '__all__' 

# 2. Serializer para Habitacion
class HabitacionSerializer(serializers.ModelSerializer):
    
    # Campo personalizado de solo lectura: 
    # Muestra el nombre completo del tipo en lugar de solo el ID.
    tipo_nombre = serializers.CharField(source='tipo.nombre', read_only=True)
    
    # Muestra el texto legible en lugar de la clave ('L' -> 'Limpia')
    estado_ocupacion_display = serializers.CharField(source='get_estado_ocupacion_display', read_only=True)
    estado_servicio_display = serializers.CharField(source='get_estado_servicio_display', read_only=True)
    
    # Usa la función que definiste en el modelo
    disponible_entrega = serializers.SerializerMethodField() 

    class Meta:
        model = Habitacion
        fields = [
            'id', 'numero', 'piso', 'tipo', 
            'tipo_nombre', 'estado_ocupacion', 'estado_ocupacion_display',
            'estado_servicio', 'estado_servicio_display', 'disponible_entrega'
        ]
        
    def get_disponible_entrega(self, obj):
        """Llama al método del modelo para ver la disponibilidad."""
        return obj.esta_disponible_para_entrega()