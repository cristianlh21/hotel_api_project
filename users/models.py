# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Agregamos campos específicos del hotel
    ROLES = [
        ('RECEPCION', 'Recepcionista'),
        ('MOZO', 'Mesero/Mozo'),
        ('GERENTE', 'Gerente'),
        ('ADMIN', 'Administrador del Sistema'),
        # Agrega más roles según necesites
    ]
    
    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default='MOZO',
        help_text='Rol del usuario dentro del hotel.',
        verbose_name='Rol de Empleado'
    )
    
    # Campo opcional para vincular con el legajo completo de RRHH
    # Lo vincularemos luego con la app 'personal'
    legajo_id = models.CharField(
        max_length=10, 
        unique=True, 
        blank=True, 
        null=True,
        help_text='Identificador único del empleado para RRHH.'
    )

    # Puedes agregar más campos necesarios aquí, como un teléfono interno.
    
    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"
