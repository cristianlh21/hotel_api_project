# reservas/models.py
from core.models import BaseModel
from django.db import models
from huespedes.models import Huesped 
# Ya NO necesitamos from habitaciones.models import Habitacion

ESTADO_CHOICES = [
    ('PEN', 'Pendiente de Confirmación'),
    ('CONF', 'Confirmada'),
    ('CI', 'Check-In Realizado'),
    ('CO', 'Check-Out Realizado'),
    ('CANC', 'Cancelada'),
    ('NS', 'No Show'),
]

class Reserva(BaseModel): # Hereda de BaseModel (UUID)
    
    huesped_titular = models.ForeignKey(
        Huesped,
        on_delete=models.PROTECT,
        related_name='reservas_titulares',
        verbose_name='Huésped Titular'
    )
    
    # ¡ATENCIÓN! Ya no hay campo 'habitacion'. La relación va en la app 'recepcion'.
    
    fecha_checkin = models.DateField(verbose_name='Fecha de Check-In')
    fecha_checkout = models.DateField(verbose_name='Fecha de Check-Out')
    
    precio_estimado = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    
    estado = models.CharField(
        max_length=4,
        choices=ESTADO_CHOICES,
        default='PEN'
    )
    
    notas = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        
    def __str__(self):
        # Ahora mostramos el estado en lugar del número de habitación
        return f"Reserva {self.id.hex[:4]}... ({self.estado})"