# inventario/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import (Proveedor, CategoriaProducto, Producto, OrdenCompra, 
                     DetalleOrdenCompra, MovimientoStock)
from .serializers import (ProveedorSerializer, CategoriaProductoSerializer, 
                          ProductoSerializer, OrdenCompraSerializer, 
                          DetalleOrdenCompraSerializer)

# --- ViewSets Maestros ---

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticated]

class CategoriaProductoViewSet(viewsets.ModelViewSet):
    queryset = CategoriaProducto.objects.all()
    serializer_class = CategoriaProductoSerializer
    permission_classes = [IsAuthenticated]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.select_related('categoria').all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

# --- ViewSet de Orden Compra (Lógica de Recepción y Stock) ---

class OrdenCompraViewSet(viewsets.ModelViewSet):
    queryset = OrdenCompra.objects.select_related('proveedor', 'creada_por').all()
    serializer_class = OrdenCompraSerializer
    permission_classes = [IsAuthenticated]

    # Lógica customizada para generar movimientos de stock al RECIBIR una OC
    def perform_update(self, serializer):
        instance = self.get_object()
        old_estado = instance.estado
        new_estado = serializer.validated_data.get('estado')

        # 🚨 Lógica crítica: Si el estado cambia a 'RECIBIDA' 🚨
        if new_estado == 'REC' and old_estado != 'REC':
            
            # 1. Guardar la orden con el nuevo estado
            serializer.save()
            
            # 2. Generar MovimientoStock para cada detalle de la orden
            user = self.request.user 
            detalles = instance.detalles.all()
            
            movimientos = []
            for detalle in detalles:
                movimientos.append(
                    MovimientoStock(
                        producto=detalle.producto,
                        tipo_movimiento='ENTRADA',
                        cantidad=detalle.cantidad_ordenada,
                        referencia_orden=instance,
                        registrado_por=user
                    )
                )
            # Guardado masivo de los movimientos
            MovimientoStock.objects.bulk_create(movimientos)
            
        else:
            # Si no hay cambio de estado a REC, guarda normalmente
            serializer.save()