# huespedes/admin.py
from django.contrib import admin
from .models import Huesped

class HuespedAdmin(admin.ModelAdmin):
    list_display = (
        'apellido', 
        'nombre', 
        'numero_documento', 
        'tipo_documento', 
        'email', 
        'telefono',
        'id' # Podemos ver el UUID generado aquí
    )
    # Permite buscar por nombre, apellido o documento
    search_fields = ('nombre', 'apellido', 'numero_documento')
    # Permite filtrar por tipo de documento y país
    list_filter = ('tipo_documento', 'pais')
    
admin.site.register(Huesped, HuespedAdmin)
