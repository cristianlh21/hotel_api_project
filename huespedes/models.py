# huespedes/models.py
from core.models import BaseModel
from django.db import models

TIPO_DOCUMENTO_CHOICES = [
    ('DNI', 'DNI/Cédula'),
    ('PAS', 'Pasaporte'),
    ('LE', 'Libreta de Enrolamiento'),
    # Agregar más tipos según el país
]

class Huesped(BaseModel): # Hereda de BaseModel (UUID)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    
    # Documentación
    tipo_documento = models.CharField(max_length=3, choices=TIPO_DOCUMENTO_CHOICES, default='DNI')
    numero_documento = models.CharField(max_length=20, unique=True, db_index=True)
    
    # Contacto
    email = models.EmailField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    
    # Dirección (Para fines legales/facturación)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, default='Argentina')
    
    # Opcional: Fecha de nacimiento, Notas, etc.

    class Meta:
        verbose_name = "Huésped"
        verbose_name_plural = "Huéspedes"
        
    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.numero_documento})"
