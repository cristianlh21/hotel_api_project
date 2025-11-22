# reservas/serializers.py
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Reserva

class ReservaSerializer(serializers.ModelSerializer):
    
    huesped_titular_nombre_completo = serializers.SerializerMethodField()
    habitacion_numero = serializers.CharField(source='habitacion.numero', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Reserva
        fields = [
            'id', 'huesped_titular', 'huesped_titular_nombre_completo', 'habitacion', 'habitacion_numero',
            'fecha_checkin', 'fecha_checkout', 'precio_estimado', 'estado', 'estado_display'
        ]

    def get_huesped_titular_nombre_completo(self, obj):
        return f"{obj.huesped_titular.nombre} {obj.huesped_titular.apellido}"

    # 🚨 LÓGICA DE NEGOCIO: VALIDACIÓN 🚨
    def validate(self, data):
        habitacion = data.get('habitacion')
        checkin = data.get('fecha_checkin')
        checkout = data.get('fecha_checkout')
        instance = self.instance 

        if checkin >= checkout:
            raise ValidationError({"fechas": "La fecha de Check-Out debe ser posterior a la fecha de Check-In."})

        # 1. Bloqueo por Mantenimiento
        if habitacion.estado_servicio == 'M':
             raise ValidationError(
                {"habitacion": "La habitación está marcada como 'En Mantenimiento' y no puede ser reservada."}
            )

        # 2. Búsqueda de Solapamiento (Permite el check-in el mismo día del checkout)
        conflictos = Reserva.objects.filter(
            habitacion=habitacion,
            estado__in=['CONF', 'CI'] 
        ).exclude(
            id=instance.id if instance else None
        ).filter(
            fecha_checkin__lt=checkout, 
            fecha_checkout__gt=checkin
        )

        if conflictos.exists():
            raise ValidationError(
                {"habitacion": "La habitación ya está reservada o con Check-In en ese período."}
            )
            
        return data

    # 🚨 LÓGICA DE NEGOCIO: GUARDADO Y CAMBIO DE ESTADO 🚨
    def create(self, validated_data):
        reserva = super().create(validated_data) 
        habitacion = validated_data['habitacion']
        
        # Cambia el estado de ocupación de la habitación a 'R' si la reserva se confirma
        if reserva.estado in ['CONF', 'PEN']:
            habitacion.estado_ocupacion = 'R' 
            habitacion.save()
            
        return reserva