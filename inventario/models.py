# inventario/models.py
from core.models import BaseModel
from django.db import models
from django.contrib.auth import get_user_model # Para registrar quién hace la OC

User = get_user_model() 

# --- A. DATOS MAESTROS ---

class Proveedor(BaseModel):
    """Información del proveedor."""
    nombre = models.CharField(max_length=150, unique=True)
    contacto_nombre = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    cuit = models.CharField(max_length=20, unique=True, verbose_name='CUIT/ID Fiscal')
    
    def __str__(self):
        return self.nombre

class CategoriaProducto(BaseModel):
    """Ej: Alimentos Frescos, Licores, Insumos de Limpieza."""
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

class Producto(BaseModel):
    """El artículo real en stock."""
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.PROTECT, related_name='productos')
    unidad_medida = models.CharField(max_length=20, help_text='Ej: Kg, Litros, Unidades, Caja')
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        unique_together = ('nombre', 'unidad_medida') # Evitar duplicados ej: 'Azúcar' en Kg y 'Azúcar' en gr
        
    def __str__(self):
        return f"{self.nombre} ({self.unidad_medida})"

# --- B. TRANSACCIONES ---

ESTADO_OC_CHOICES = [
    ('PEND', 'Pendiente de Aprobación'),
    ('APR', 'Aprobada/Enviada'),
    ('REC', 'Recibida Parcial/Completa'),
    ('CANC', 'Cancelada'),
]

TIPO_MOVIMIENTO_CHOICES = [
    ('ENTRADA', 'Entrada por Compra'),
    ('SALIDA', 'Salida por Consumo/Venta'),
    ('AJUSTE', 'Ajuste de Inventario'),
]

class OrdenCompra(BaseModel):
    """Encabezado de la orden de compra."""
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='ordenes')
    fecha_orden = models.DateField(auto_now_add=True)
    fecha_estimada_entrega = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=4, choices=ESTADO_OC_CHOICES, default='PEND')
    creada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"OC {self.id.hex[:4]}... - {self.proveedor.nombre}"

class DetalleOrdenCompra(BaseModel):
    """Cada línea de producto dentro de una Orden de Compra."""
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad_ordenada = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad_ordenada}"

class MovimientoStock(BaseModel):
    """
    Registro que afecta el stock (la fuente de la verdad para el stock actual).
    """
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='movimientos')
    tipo_movimiento = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO_CHOICES)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, help_text='Cantidad que entra (+) o sale (-)')
    referencia_orden = models.ForeignKey(OrdenCompra, on_delete=models.SET_NULL, null=True, blank=True)
    ubicacion = models.CharField(max_length=50, default='Almacén Principal')
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.tipo_movimiento} de {self.cantidad} {self.producto.nombre}"