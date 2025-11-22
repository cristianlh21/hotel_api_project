# reservas/admin.py
from django.contrib import admin
from .models import Reserva

class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'huesped_titular', 
        'estado', 
        'fecha_checkin', 
        'fecha_checkout', 
        'habitaciones_asignadas', # <- Muestra las habitaciones vía Estadías
        'precio_estimado'
    )
    list_filter = ('estado', 'fecha_checkin')
    search_fields = ('huesped_titular__apellido', 'id')

    def habitaciones_asignadas(self, obj):
        # Accede a las Estadías (relación inversa 'estadias' definida en recepcion/models.py)
        numeros = obj.estadias.values_list('habitacion__numero', flat=True)
        return ", ".join(numeros)
        
    habitaciones_asignadas.short_description = 'Habitaciones Asignadas'

admin.site.register(Reserva, ReservaAdmin)