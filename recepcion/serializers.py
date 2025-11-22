# recepcion/serializers.py
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Estadia, HuespedEstadia
from reservas.models import Reserva # Para la validación de la reserva padre

# --- 1. HUESPED ESTADIA (Ocupantes) ---
class HuespedEstadiaSerializer(serializers.ModelSerializer):
    huesped_nombre_completo = serializers.CharField(source='huesped.get_full_name', read_only=True)
    
    class Meta:
        model = HuespedEstadia
        fields = ['id', 'estadia', 'huesped', 'es_principal', 'huesped_nombre_completo']
        read_only_fields = ['id', 'estadia']

# --- 2. ESTADIA (El que bloquea la habitación) ---
class EstadiaSerializer(serializers.ModelSerializer):
    
    ocupantes = HuespedEstadiaSerializer(many=True, read_only=True)
    habitacion_numero = serializers.CharField(source='habitacion.numero', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Estadia
        fields = '__all__'
        read_only_fields = ('checkin_timestamp', 'checkout_timestamp')

    # 🚨 LÓGICA CLAVE DE VALIDACIÓN Y BLOQUEO 🚨
    def validate(self, data):
        """Verifica que la habitación esté disponible y no en mantenimiento."""
        
        habitacion = data.get('habitacion')
        reserva = data.get('reserva')
        checkin = reserva.fecha_checkin # Las fechas vienen de la Reserva Padre
        checkout = reserva.fecha_checkout
        instance = self.instance # Para exclusión en caso de UPDATE

        # 1. Bloqueo por Mantenimiento (Regla del negocio)
        if habitacion.estado_servicio == 'M':
             raise ValidationError(
                {"habitacion": "Esta habitación está en Mantenimiento y no puede ser asignada."}
            )

        # 2. Búsqueda de Solapamiento con otras Estadías activas
        conflictos = Estadia.objects.filter(
            habitacion=habitacion,
            estado__in=['PEND', 'ACT'] # Consideramos 'Pendiente' y 'Activa' como bloqueo
        ).exclude(
            id=instance.id if instance else None
        ).filter(
            fecha_checkin__lt=checkout, 
            fecha_checkout__gt=checkin
        )

        if conflictos.exists():
            raise ValidationError(
                {"habitacion": "La habitación ya tiene una Estadía o Reserva confirmada en ese periodo."}
            )
            
        return data

    def create(self, validated_data):
        """Guarda la estadía y actualiza el estado de la habitación a 'Reservada'."""
        
        estadia = super().create(validated_data) 
        habitacion = validated_data['habitacion']
        
        # 🚨 CAMBIO DE ESTADO: La estadía se crea, la habitación pasa a 'Reservada'
        if estadia.estado == 'PEND':
            habitacion.estado_ocupacion = 'R' 
            habitacion.save()
            
        return estadia