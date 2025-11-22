# personal/models.py
from core.models import BaseModel
from django.db import models
from django.conf import settings # Para acceder al AUTH_USER_MODEL

# --- 1. DATOS MAESTROS (Estructura de la empresa) ---

class Departamento(BaseModel):
    """Ej: Recepción, Cocina, Mantenimiento."""
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

class Puesto(BaseModel):
    """Ej: Jefe de Cocina, Recepcionista Senior, Mucama."""
    nombre = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='puestos')
    salario_base_mensual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        unique_together = ('nombre', 'departamento')
        
    def __str__(self):
        return f"{self.nombre} ({self.departamento.nombre})"

# --- 2. EL LEGAJO (Datos del empleado) ---

class Empleado(BaseModel):
    """
    Legajo del empleado. Contiene datos personales y la relación con el sistema de login.
    """
    # Relación 1-a-1 con la cuenta de login (para que el empleado pueda fichar)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='legajo',
        verbose_name='Usuario del Sistema'
    )
    puesto = models.ForeignKey(Puesto, on_delete=models.PROTECT, related_name='empleados')
    
    fecha_contratacion = models.DateField()
    numero_legajo = models.CharField(max_length=20, unique=True)
    
    # Datos personales
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"Legajo {self.numero_legajo}: {self.apellido}, {self.nombre}"

# --- 3. DATOS TRANSACCIONALES (Control de Tiempo) ---

class HorarioTurno(BaseModel):
    """Define un turno predefinido (ej: 'Mañana 8:00-16:00')."""
    nombre = models.CharField(max_length=50, unique=True)
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()
    
    def __str__(self):
        return self.nombre

class Asistencia(BaseModel):
    """
    Registro de fichaje (reloj). Se usa para calcular las horas trabajadas.
    """
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='asistencias')
    
    # Campo para registrar la entrada y salida de manera precisa
    hora_entrada_real = models.DateTimeField()
    hora_salida_real = models.DateTimeField(null=True, blank=True)
    
    # Opcional: Puede estar asociado a un turno para fines de auditoría
    turno_asignado = models.ForeignKey(HorarioTurno, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Asistencia de {self.empleado.apellido} en {self.hora_entrada_real.date()}"