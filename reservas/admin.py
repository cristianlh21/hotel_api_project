# reservas/admin.py
from django.contrib import admin
from .models import Reserva

class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'huesped_titular', 
        'habitacion', 
        'fecha_checkin', 
        'fecha_checkout', 
        'estado', 
        'precio_estimado'
    )
    list_filter = ('estado', 'habitacion__tipo', 'fecha_checkin')
    search_fields = ('huesped_titular__apellido', 'habitacion__numero', 'id')
    date_hierarchy = 'fecha_checkin' # Permite navegar por fechas

admin.site.register(Reserva, ReservaAdmin)
