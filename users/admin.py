# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# 🚨 IMPORTANTE: Necesitamos importar el modelo Empleado para el Inline
from personal.models import Empleado 


# 1. Definir el Inline (Formulario de Empleado dentro del Usuario)
class EmpleadoInline(admin.StackedInline):
    """Permite crear o editar el Legajo del Empleado desde el formulario de Usuario."""
    model = Empleado
    can_delete = False
    verbose_name_plural = 'Datos del Legajo (RRHH)'
    fk_name = 'usuario' # Especifica la clave foránea a usar (el OneToOneField)
    # Campos que queremos mostrar en el inline (Ocultamos el campo 'usuario' que es automático)
    fields = ('puesto', 'numero_legajo', 'dni', 'fecha_contratacion', 'nombre', 'apellido')


# 2. Modificar el Admin de CustomUser
class CustomUserAdmin(UserAdmin):
    # Campos a mostrar en la lista de usuarios
    list_display = UserAdmin.list_display + ('rol',)
    
    # Campos para editar en el formulario (añadimos 'rol')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('rol', 'legajo_id')}),
    )
    
    # ¡Añadir el Inline! Ahora, al crear un CustomUser, aparecerá el formulario Empleado.
    inlines = (EmpleadoInline,)


admin.site.register(CustomUser, CustomUserAdmin)