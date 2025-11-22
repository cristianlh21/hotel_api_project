# cuentas/models.py
from core.models import BaseModel
from django.db import models
from reservas.models import Reserva # Importamos la Reserva

ESTADO_CUENTA_CHOICES = [
    ('ABT', 'Abierta'), # Activa, esperando consumos
    ('CERR', 'Cerrada'), # Facturada, pendiente de pago (si queda saldo)
    ('PAG', 'Pagada') # Saldo en cero
]

TIPO_TRANSACCION_CHOICES = [
    ('CARGO', 'Cargo (Consumo/Tarifa)'), # Debito
    ('PAGO', 'Pago (Efectivo/Tarjeta)'), # Crédito
]

# --- MODELO 1: CUENTA (EL FOLIO/LEDGER) ---
class Cuenta(BaseModel):
    """
    Representa el Folio o la Cuenta Corriente activa de una estadía/reserva.
    """
    reserva = models.OneToOneField(
        Reserva,
        on_delete=models.PROTECT,
        related_name='cuenta',
        verbose_name='Reserva Asociada'
    )
    estado = models.CharField(
        max_length=4,
        choices=ESTADO_CUENTA_CHOICES,
        default='ABT'
    )
    # Se puede agregar campos de saldo, pero es mejor calcularlo con las transacciones.

    class Meta:
        verbose_name = "Cuenta de Huésped"
        verbose_name_plural = "Cuentas de Huéspedes"
    
    def __str__(self):
        return f"Cuenta {self.id} - Reserva {self.reserva.habitacion.numero}"


# --- MODELO 2: TRANSACCION (EL MOVIMIENTO) ---
class Transaccion(BaseModel):
    """
    Representa un movimiento de débito (cargo) o crédito (pago) en la cuenta.
    """
    cuenta = models.ForeignKey(
        Cuenta,
        on_delete=models.CASCADE, # Si se borra la cuenta, se borran las transacciones
        related_name='transacciones',
        verbose_name='Cuenta'
    )
    tipo = models.CharField(
        max_length=5,
        choices=TIPO_TRANSACCION_CHOICES
    )
    concepto = models.CharField(
        max_length=150,
        help_text='Detalle del cargo o pago (Ej: Tarifa, Restaurante, Depósito, Lavandería).'
    )
    monto = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text='Monto de la transacción.'
    )
    
    def __str__(self):
        return f"{self.tipo}: {self.monto} en Cuenta {self.cuenta.id}"