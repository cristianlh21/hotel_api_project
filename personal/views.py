# personal/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Departamento, Puesto, Empleado
from .serializers import DepartamentoSerializer, PuestoSerializer, EmpleadoSerializer

User = get_user_model() # Obtiene el CustomUser

# --- ViewSets Simples ---
class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

class PuestoViewSet(viewsets.ModelViewSet):
    queryset = Puesto.objects.select_related('departamento').all()
    serializer_class = PuestoSerializer

# --- ViewSet con Lógica de Creación Anidada (CRUCIAL) ---

class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.select_related('puesto', 'usuario').all()
    serializer_class = EmpleadoSerializer

    def create(self, request, *args, **kwargs):
        """
        Método customizado para crear el CustomUser Y el Empleado a partir de un solo payload.
        """
        data = request.data
        usuario_data = data.pop('usuario_data', None) # Extraer los datos del usuario del payload
        
        if not usuario_data:
            return Response({"usuario_data": "Se requieren los datos de usuario para crear el login."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        # 1. Crear el CustomUser
        try:
            username = usuario_data.get('username')
            password = usuario_data.get('password')
            rol = usuario_data.get('rol', 'MOZO') # Asignar un rol por defecto
            
            user = User.objects.create_user(
                username=username,
                password=password,
                rol=rol # Usamos el campo personalizado de nuestro CustomUser
            )
            
        except Exception as e:
            return Response({"usuario": f"Error al crear el usuario: {str(e)}"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # 2. Crear el Empleado, asignando el ID del usuario recién creado
        try:
            # Añadimos el ID del usuario creado a los datos del empleado antes de serializar
            data['usuario'] = user.id 
            
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            
            # Devolver la respuesta final con el objeto Empleado creado
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            
        except Exception as e:
            # Si la creación del Empleado falla, debemos eliminar el Usuario que ya creamos
            user.delete() 
            return Response({"empleado": f"Error al crear el legajo: {str(e)}"}, 
                            status=status.HTTP_400_BAD_REQUEST)