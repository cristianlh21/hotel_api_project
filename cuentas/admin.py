# cuentas/admin.py
from django.contrib import admin
from django.db import models # Necesario para models.Sum
from .models import Cuenta, Transaccion

class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('cuenta_info', 'tipo', 'concepto', 'monto', 'created_at')
    list_filter = ('tipo', 'cuenta__estado')
    search_fields = ('concepto', 'cuenta__reserva__habitacion__numero')
    
    def cuenta_info(self, obj):
        return f"Cuenta {obj.cuenta.id.hex[:4]}... - Hab. {obj.cuenta.reserva.habitacion.numero}"
    cuenta_info.short_description = 'Cuenta'

class CuentaAdmin(admin.ModelAdmin):
    list_display = ('reserva_info', 'estado', 'saldo_actual', 'created_at')
    list_filter = ('estado',)
    search_fields = ('reserva__habitacion__numero', 'reserva__huesped_titular__apellido')
    raw_id_fields = ('reserva',) # Facilita la búsqueda de la Reserva por ID

    # Método para calcular y mostrar el saldo en el panel
    def saldo_actual(self, obj):
        """Calcula el saldo: Cargos - Pagos."""
        
        # Consulta optimizada para sumar todos los cargos
        cargos = obj.transacciones.filter(tipo='CARGO').aggregate(
            total=models.Sum('monto')
        )['total'] or 0
        
        # Consulta optimizada para sumar todos los pagos
        pagos = obj.transacciones.filter(tipo='PAGO').aggregate(
            total=models.Sum('monto')
        )['total'] or 0
        
        balance = cargos - pagos
        
        # Retornar el saldo con formato de moneda
        return f"${balance:,.2f}"

    saldo_actual.short_description = 'Saldo Actual'
    
    def reserva_info(self, obj):
        return f"Reserva Hab. {obj.reserva.habitacion.numero}"
    reserva_info.short_description = 'Reserva'

admin.site.register(Cuenta, CuentaAdmin)
admin.site.register(Transaccion, TransaccionAdmin)