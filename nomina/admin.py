# nomina/admin.py
from django.contrib import admin
from .models import ConceptoNomina, Liquidacion, DetalleLiquidacion

# Inline para ver los detalles del recibo dentro de la liquidación
class DetalleLiquidacionInline(admin.TabularInline):
    model = DetalleLiquidacion
    extra = 0
    readonly_fields = ('concepto', 'monto', 'cantidad') # Los detalles no se editan post-cálculo
    can_delete = False

class LiquidacionAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'fecha_inicio_periodo', 'fecha_fin_periodo', 'monto_neto', 'estado')
    list_filter = ('estado', 'fecha_fin_periodo')
    search_fields = ('empleado__apellido', 'empleado__numero_legajo')
    date_hierarchy = 'fecha_fin_periodo'
    raw_id_fields = ('empleado',)
    inlines = [DetalleLiquidacionInline]
    
    # Impedir la edición manual de los montos totales (solo se actualizan con el cálculo)
    readonly_fields = ('monto_bruto', 'monto_neto', 'empleado', 'fecha_inicio_periodo', 'fecha_fin_periodo')
    
admin.site.register(ConceptoNomina)
admin.site.register(Liquidacion, LiquidacionAdmin)