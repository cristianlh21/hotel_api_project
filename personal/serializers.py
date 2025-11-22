# personal/serializers.py
from rest_framework import serializers
from .models import Departamento, Puesto, Empleado, HorarioTurno, Asistencia

# --- Serializadores de Datos Maestros ---

class DepartamentoSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Departamento
        fields = '__all__'

class PuestoSerializer(serializers.ModelSerializer):
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Puesto
        fields = '__all__'
        read_only_fields = ('salario_base_mensual',) # Se maneja en el Puesto

# --- Serializador del Empleado ---

class EmpleadoSerializer(serializers.ModelSerializer):
    # Campos de lectura para el ViewSet
    puesto_nombre = serializers.CharField(source='puesto.nombre', read_only=True)
    nombre_usuario = serializers.CharField(source='usuario.username', read_only=True)
    id = serializers.UUIDField(read_only=True)
    
    # Campo de ESCRITURA: Aquí se enviarán los datos del Usuario desde el frontend (temporalmente)
    # Lo marcaremos como opcional, ya que será manejado por el ViewSet
    usuario_data = serializers.JSONField(write_only=True, required=False) 

    class Meta:
        model = Empleado
        fields = '__all__'
        read_only_fields = ('usuario',) # El campo FK de usuario no debe ser editable directamente