# recepcion/admin.py
from django.contrib import admin
from .models import Estadia, HuespedEstadia

# --- Inline para gestionar los Ocupantes ---
class HuespedEstadiaInline(admin.TabularInline):
    """
    Permite añadir o editar los acompañantes directamente dentro del formulario de Estadia.
    """
    model = HuespedEstadia
    extra = 1 # Muestra un campo vacío adicional por defecto
    raw_id_fields = ('huesped',) # Usamos raw_id_fields para el UUID del Huesped

# --- 1. Admin para Estadia ---
class EstadiaAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'reserva', 
        'habitacion', 
        'estado', 
        'checkin_timestamp', 
        'checkout_timestamp'
    )
    list_filter = ('estado', 'habitacion__tipo')
    search_fields = ('reserva__huesped_titular__apellido', 'habitacion__numero')
    
    # raw_id_fields es esencial para manejar UUIDs y IDs de otras tablas de forma eficiente
    raw_id_fields = ('reserva', 'habitacion') 
    
    # Agregamos la clase Inline para el listado de ocupantes
    inlines = [HuespedEstadiaInline] 

# --- 2. Admin para HuespedEstadia (Ocupantes) ---
class HuespedEstadiaAdmin(admin.ModelAdmin):
    list_display = (
        'huesped_info', 
        'estadia_info', 
        'es_principal',
        'created_at'
    )
    list_filter = ('es_principal',)
    search_fields = ('huesped__apellido', 'estadia__habitacion__numero')
    raw_id_fields = ('estadia', 'huesped')

    def estadia_info(self, obj):
        return f"Estadía Hab. {obj.estadia.habitacion.numero}"
    estadia_info.short_description = 'Estadía'
    
    def huesped_info(self, obj):
        return f"{obj.huesped.apellido}, {obj.huesped.nombre}"
    huesped_info.short_description = 'Huésped'

# Registrar los modelos
admin.site.register(Estadia, EstadiaAdmin)
admin.site.register(HuespedEstadia, HuespedEstadiaAdmin)
