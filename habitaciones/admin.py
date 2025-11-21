# habitaciones/admin.py
from django.contrib import admin
from .models import TipoHabitacion, Habitacion

# Opcional: Personalizar la visualización de las habitaciones en el panel
class HabitacionAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista
    list_display = ('numero', 'piso', 'tipo', 'estado_ocupacion', 'estado_servicio', 'esta_disponible_para_entrega')
    
    # Filtros laterales
    list_filter = ('piso', 'tipo', 'estado_ocupacion', 'estado_servicio')
    
    # Campos de búsqueda
    search_fields = ('numero', 'tipo__nombre')
    
    # Campos que se pueden editar directamente en la lista
    list_editable = ('estado_ocupacion', 'estado_servicio')

# 1. Registra el modelo TipoHabitacion
admin.site.register(TipoHabitacion)

# 2. Registra el modelo Habitacion usando la clase personalizada
admin.site.register(Habitacion, HabitacionAdmin)