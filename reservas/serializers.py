# reservas/serializers.py
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Reserva

class ReservaSerializer(serializers.ModelSerializer):
    
    # Campo para contar las habitaciones asignadas (Estadías)
    cantidad_habitaciones = serializers.SerializerMethodField()
    huesped_titular_nombre_completo = serializers.SerializerMethodField()
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Reserva
        fields = [
            'id', 'huesped_titular', 'huesped_titular_nombre_completo', 
            'cantidad_habitaciones', 
            'fecha_checkin', 'fecha_checkout', 
            'precio_estimado', 'estado', 'estado_display'
        ]

    def get_huesped_titular_nombre_completo(self, obj):
        return f"{obj.huesped_titular.nombre} {obj.huesped_titular.apellido}"
    
    def get_cantidad_habitaciones(self, obj):
        # Cuenta cuántas Estadías (Habitaciones asignadas en la nueva app 'recepcion') tiene esta reserva
        return obj.estadias.count() 

    # Validación simplificada (Solo verifica que Checkout sea después de Checkin)
    def validate(self, data):
        checkin = data.get('fecha_checkin')
        checkout = data.get('fecha_checkout')
        
        if checkin >= checkout:
            raise ValidationError({"fechas": "La fecha de Check-Out debe ser posterior a la fecha de Check-In."})

        # Toda la lógica compleja de disponibilidad se MOVIÓ al EstadiaSerializer (que viene después).
        return data
    
    def create(self, validated_data):
        # El método create es simple: solo guarda la Reserva, sin tocar la Habitación.
        reserva = super().create(validated_data) 
        return reserva