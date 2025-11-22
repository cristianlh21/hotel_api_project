# huespedes/serializers.py
from rest_framework import serializers
from .models import Huesped

class HuespedSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Huesped.
    Mapea todos los campos del modelo a JSON para el API.
    """
    # Campo de solo lectura para mostrar el nombre del tipo de documento 
    # en lugar de la clave corta (ej: 'DNI' en lugar de 'DNI')
    tipo_documento_display = serializers.CharField(source='get_tipo_documento_display', read_only=True)

    class Meta:
        model = Huesped
        # fields = '__all__' es la opción más sencilla para incluir todos los campos.
        fields = '__all__'
        # Los campos que queremos que solo se puedan leer (ej. el ID y las fechas de creación)
        read_only_fields = ('id', 'created_at', 'updated_at')