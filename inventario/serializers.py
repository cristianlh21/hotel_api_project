# inventario/serializers.py
from rest_framework import serializers
from django.db.models import Sum
from .models import (Proveedor, CategoriaProducto, Producto, OrdenCompra, 
                     DetalleOrdenCompra, MovimientoStock)

# --- Serializers Maestros ---

class ProveedorSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Proveedor
        fields = '__all__'

class CategoriaProductoSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = CategoriaProducto
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    stock_actual = serializers.SerializerMethodField() # <<< CAMPO CALCULADO

    class Meta:
        model = Producto
        fields = '__all__'
        
    def get_stock_actual(self, obj):
        """Calcula el stock actual sumando todos los MovimientosStock relacionados."""
        # Sumamos el campo 'cantidad' de todos los movimientos (las salidas serán negativas)
        total = obj.movimientos.aggregate(total=Sum('cantidad'))['total']
        return total if total is not None else 0

# --- Serializers Transaccionales ---

class DetalleOrdenCompraSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    class Meta:
        model = DetalleOrdenCompra
        fields = '__all__'
        read_only_fields = ['orden'] # 'orden' se asigna en el ViewSet

class OrdenCompraSerializer(serializers.ModelSerializer):
    detalles = DetalleOrdenCompraSerializer(many=True, read_only=True)
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta:
        model = OrdenCompra
        fields = '__all__'
        read_only_fields = ['creada_por']