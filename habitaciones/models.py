from django.db import models

class TipoHabitacion(models.Model):
    nombre = models.CharField(max_length=50, unique=True)  # Ej: 'Doble Matrimonial', 'Suite Deluxe'
    descripcion = models.TextField(blank=True, null=True)
    capacidad_maxima = models.PositiveSmallIntegerField(default=2)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Define si este tipo de habitación es convertible (ej: doble matrimonial -> doble twin)
    es_convertible = models.BooleanField(default=False) 
    
    def __str__(self):
        return self.nombre
    
PISOS_CHOICES = [
    ('PB', 'Planta Baja'),
    ('1', 'Primer Piso'),
    ('2', 'Segundo Piso'),
    ('3', 'Tercer Piso'),
    ('4', 'Cuarto Piso'),
    # Agrega más si es necesario...
]

ESTADO_OCUPACION_CHOICES = [
    ('L', 'Libre'),
    ('R', 'Reservada'),
    ('O', 'Ocupada'),
]

ESTADO_LIMPIEZA_CHOICES = [
    ('L', 'Limpia'),
    ('S', 'Sucia'),
    ('E', 'En Limpieza'),
    ('M', 'En Mantenimiento'),
]

class Habitacion(models.Model):
    numero = models.CharField(max_length=10, unique=True, verbose_name='Número de Habitación')
    piso = models.CharField(max_length=2, choices=PISOS_CHOICES)
    tipo = models.ForeignKey(TipoHabitacion, on_delete=models.PROTECT) # PROTECT previene borrar tipos si tienen habitaciones asociadas

    # --- ESTADOS OPERACIONALES CLAVE ---
    
    # 1. Estado de Ocupación (Lo que el huésped puede hacer)
    estado_ocupacion = models.CharField(
        max_length=1,
        choices=ESTADO_OCUPACION_CHOICES,
        default='L',
        verbose_name='Estado de Ocupación'
    )
    
    # 2. Estado de Servicio/Mantenimiento (Lo que el personal debe hacer)
    estado_servicio = models.CharField(
        max_length=1,
        choices=ESTADO_LIMPIEZA_CHOICES,
        default='L',
        verbose_name='Estado de Limpieza/Servicio'
    )
    
    def esta_disponible_para_entrega(self):
        """Define la disponibilidad real para un nuevo huésped."""
        return self.estado_ocupacion == 'L' and self.estado_servicio == 'L'

    def __str__(self):
        return f"Hab. {self.numero} - {self.get_estado_ocupacion_display()}"   
