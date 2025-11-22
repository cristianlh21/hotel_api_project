# inventario/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (ProveedorViewSet, CategoriaProductoViewSet, 
                    ProductoViewSet, OrdenCompraViewSet)

router = DefaultRouter()

router.register(r'proveedores', ProveedorViewSet)
router.register(r'categorias', CategoriaProductoViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'ordenescompra', OrdenCompraViewSet)

urlpatterns = [
    path('', include(router.urls)),
]