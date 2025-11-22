# recepcion/models.py
from core.models import BaseModel
from django.db import models
from reservas.models import Reserva
from habitaciones.models import Habitacion
from huespedes.models import Huesped

class Estadia(BaseModel):
    """
    Representa la asignación de una habitación específica dentro de una Reserva.
    Una Reserva puede tener múltiples Estadías (ej: Reserva de 3 habitaciones).
    """
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.CASCADE, # Si la reserva se borra, la estadía asociada se borra.
        related_name='estadias',
        verbose_name='Reserva Padre'
    )
    habitacion = models.ForeignKey(
        Habitacion,
        on_delete=models.PROTECT,
        related_name='estadias',
        verbose_name='Habitación Asignada'
    )
    
    # Fechas de la estadía (se copian de la reserva, pero son operacionales)
    fecha_checkin = models.DateField()
    fecha_checkout = models.DateField()
    
    # Sellos de tiempo exactos (para el cálculo de la permanencia y auditoría)
    checkin_timestamp = models.DateTimeField(null=True, blank=True)
    checkout_timestamp = models.DateTimeField(null=True, blank=True)
    
    ESTADO_CHOICES = [
        ('PEND', 'Pendiente Check-In'), 
        ('ACT', 'Activa (Huéspedes en habitación)'), 
        ('FINAL', 'Finalizada (Check-Out completo)')
    ]
    estado = models.CharField(max_length=5, choices=ESTADO_CHOICES, default='PEND')

    def __str__(self):
        return f"Estadía {self.id.hex[:4]}... - Hab. {self.habitacion.numero}"
    
# recepcion/models.py (Añadir al final del archivo)

class HuespedEstadia(BaseModel):
    """
    Modelo intermedio que registra a todos los ocupantes de una Habitación/Estadía.
    """
    estadia = models.ForeignKey(
        Estadia,
        on_delete=models.CASCADE, # Si la estadía se borra, se borra la lista de ocupantes
        related_name='ocupantes',
        verbose_name='Estadía Asociada'
    )
    huesped = models.ForeignKey(
        Huesped,
        on_delete=models.PROTECT,
        related_name='estadias_ocupadas',
        verbose_name='Huésped'
    )
    # Flag para identificar el huésped principal de la habitación (el que firma el folio)
    es_principal = models.BooleanField(
        default=False, 
        help_text='Indica si esta persona es el responsable principal de la habitación.'
    )

    class Meta:
        verbose_name = "Ocupante de Estadía"
        verbose_name_plural = "Ocupantes de Estadía"
        # Garantiza que un huésped no figure dos veces en la misma habitación al mismo tiempo
        unique_together = ('estadia', 'huesped')

    def __str__(self):
        return f"Ocupante: {self.huesped.apellido} en Hab. {self.estadia.habitacion.numero}"