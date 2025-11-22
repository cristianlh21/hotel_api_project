# personal/admin.py
from django.contrib import admin
from .models import Departamento, Puesto, Empleado, HorarioTurno, Asistencia

# --- Datos Maestros ---
admin.site.register(Departamento)

class PuestoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento', 'salario_base_mensual')
    list_filter = ('departamento',)
admin.site.register(Puesto, PuestoAdmin)

admin.site.register(HorarioTurno)

# --- Modelo de Asistencia ---
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'hora_entrada_real', 'hora_salida_real', 'turno_asignado')
    list_filter = ('empleado__puesto__departamento',)
    date_hierarchy = 'hora_entrada_real'
admin.site.register(Asistencia, AsistenciaAdmin)


# --- Modelo de Empleado (Legajo) ---
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('numero_legajo', 'apellido', 'nombre', 'puesto', 'dni', 'fecha_contratacion')
    list_filter = ('puesto__departamento', 'puesto')
    search_fields = ('numero_legajo', 'dni', 'apellido', 'nombre')
    raw_id_fields = ('usuario', 'puesto') # raw_id para IDs complejos
admin.site.register(Empleado, EmpleadoAdmin)