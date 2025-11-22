# inventario/admin.py
from django.contrib import admin
from django.db.models import Sum # Necesario para calcular el stock total
from .models import (Proveedor, CategoriaProducto, Producto, OrdenCompra, 
                     DetalleOrdenCompra, MovimientoStock)

# --- INLINES ---

class DetalleOrdenCompraInline(admin.TabularInline):
    """Permite añadir los productos de la OC directamente en el formulario de OrdenCompra."""
    model = DetalleOrdenCompra
    extra = 1
    raw_id_fields = ('producto',) 

# --- MODEL ADMINS ---

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'unidad_medida', 'stock_actual', 'stock_minimo')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'unidad_medida')
    raw_id_fields = ('categoria',)

    def stock_actual(self, obj):
        """
        Calcula el stock actual y lo muestra con colores/emojis si está bajo el mínimo.
        """
        # Sumamos el campo 'cantidad' de todos los movimientos
        total = obj.movimientos.aggregate(total=Sum('cantidad'))['total']
        
        if total is None:
            total = 0
            
        # Lógica de coloración para alertas operacionales
        if total < obj.stock_minimo:
            # Stock Crítico
            return f"🚨 {total} {obj.unidad_medida}"
        elif total < obj.stock_minimo * 1.5:
            # Stock Bajo
            return f"⚠️ {total} {obj.unidad_medida}"
        return f"{total} {obj.unidad_medida}"

    stock_actual.short_description = 'Stock Actual'
    stock_actual.allow_tags = True # Necesario para renderizar los emojis en el Admin

class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'proveedor', 'fecha_orden', 'estado', 'creada_por')
    list_filter = ('estado', 'proveedor')
    search_fields = ('proveedor__nombre', 'id')
    date_hierarchy = 'fecha_orden'
    raw_id_fields = ('proveedor', 'creada_por')
    inlines = [DetalleOrdenCompraInline]

# --- REGISTRO ---

admin.site.register(Proveedor)
admin.site.register(CategoriaProducto)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(OrdenCompra, OrdenCompraAdmin)
admin.site.register(MovimientoStock)
