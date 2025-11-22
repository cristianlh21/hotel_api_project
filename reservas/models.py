# reservas/models.py
from core.models import BaseModel
from django.db import models
from habitaciones.models import Habitacion
from huespedes.models import Huesped # Importamos el modelo de la app huespedes

ESTADO_CHOICES = [
    ('PEN', 'Pendiente de Confirmación'),
    ('CONF', 'Confirmada'),
    ('CI', 'Check-In Realizado'),
    ('CO', 'Check-Out Realizado'),
    ('CANC', 'Cancelada'),
    ('NS', 'No Show'),
]

class Reserva(BaseModel): # Hereda de BaseModel (UUID)
    # --- RELACIONES ---
    
    # 1. Huésped Titular (La persona o intermediario que hizo el booking)
    huesped_titular = models.ForeignKey(
        Huesped,
        on_delete=models.PROTECT, # No borramos un huésped si tiene reservas
        related_name='reservas_titulares',
        verbose_name='Huésped Titular'
    )
    
    # 2. Habitación Asignada (La habitación que se bloquea)
    habitacion = models.ForeignKey(
        Habitacion,
        on_delete=models.PROTECT,
        related_name='reservas',
        verbose_name='Habitación Asignada'
    )
    
    # --- FECHAS Y TIEMPO ---
    fecha_checkin = models.DateField(verbose_name='Fecha de Check-In')
    fecha_checkout = models.DateField(verbose_name='Fecha de Check-Out')
    
    # --- DATOS FINANCIEROS Y OPERACIONALES ---
    precio_estimado = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text='Precio total de la estadía sin incluir extras.'
    )
    
    # Estado Operacional
    estado = models.CharField(
        max_length=4,
        choices=ESTADO_CHOICES,
        default='PEN',
        verbose_name='Estado de la Reserva'
    )
    
    notas = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        
    def __str__(self):
        return f"Reserva {self.id} - Hab. {self.habitacion.numero} ({self.estado})"
