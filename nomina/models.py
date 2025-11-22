# nomina/models.py
from core.models import BaseModel
from django.db import models
from personal.models import Empleado

# --- 1. DATOS MAESTROS (Conceptos) ---

TIPO_CONCEPTO_CHOICES = [
    ('INGRESO', 'Ingreso (Sueldo, Bono, Extra)'),
    ('EGRESO', 'Egreso (Retención, Impuesto, Adelanto)'),
]

class ConceptoNomina(BaseModel):
    """Define un ítem de la liquidación (ej: Sueldo Base, Horas Extra, Retención Jubilatoria)."""
    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=7, choices=TIPO_CONCEPTO_CHOICES)
    es_calculado = models.BooleanField(
        default=False, 
        help_text='Indica si el monto debe ser calculado por el sistema (ej: Horas Extra) o es un valor fijo.'
    )
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

# --- 2. LA LIQUIDACIÓN FINAL ---

ESTADO_LIQUIDACION_CHOICES = [
    ('PEND', 'Pendiente de Revisión'),
    ('APRO', 'Aprobada/Lista para Pago'),
    ('PAG', 'Pagada'),
    ('CANC', 'Cancelada'),
]

class Liquidacion(BaseModel):
    """
    Registro final de pago para un empleado en un período específico.
    """
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT, related_name='liquidaciones')
    
    fecha_inicio_periodo = models.DateField()
    fecha_fin_periodo = models.DateField()
    
    monto_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monto_neto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    estado = models.CharField(max_length=4, choices=ESTADO_LIQUIDACION_CHOICES, default='PEND')
    
    class Meta:
        # Un empleado solo puede tener una liquidación activa por período
        unique_together = ('empleado', 'fecha_inicio_periodo', 'fecha_fin_periodo')
        
    def __str__(self):
        return f"Liq. {self.empleado.apellido} de {self.fecha_inicio_periodo} a {self.fecha_fin_periodo}"

# --- 3. DETALLE DE LA LIQUIDACIÓN (Líneas del recibo) ---

class DetalleLiquidacion(BaseModel):
    """
    Cada línea de ingreso o egreso que compone el recibo de sueldo.
    """
    liquidacion = models.ForeignKey(Liquidacion, on_delete=models.CASCADE, related_name='detalles')
    concepto = models.ForeignKey(ConceptoNomina, on_delete=models.PROTECT)
    
    # Monto calculado para esta línea
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Campo opcional para registrar horas, días, o unidades (ej: 160 horas trabajadas)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.concepto.nombre}: {self.monto}"