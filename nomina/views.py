# nomina/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from .models import ConceptoNomina, Liquidacion, DetalleLiquidacion
from .serializers import LiquidacionSerializer, DetalleLiquidacionSerializer, ConceptoNominaSerializer
from personal.models import Empleado, Asistencia, Puesto # Importar datos para el cálculo
from decimal import Decimal
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers


class ConceptoNominaViewSet(viewsets.ModelViewSet):
    queryset = ConceptoNomina.objects.all()
    # 🚨 CAMBIAR ESTO:
    serializer_class = ConceptoNominaSerializer # <<<--- USAR EL SERIALIZER CORRECTO
    permission_classes = [IsAuthenticated]

# --- ViewSet con Lógica de Cálculo (Crucial) ---
class LiquidacionViewSet(viewsets.ModelViewSet):
    queryset = Liquidacion.objects.select_related('empleado', 'empleado__puesto').all()
    serializer_class = LiquidacionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], url_path='calcular')
    def calcular_liquidacion(self, request):
        """
        API para calcular una liquidación de un empleado en un rango de fechas.
        Recibe: empleado_id, fecha_inicio, fecha_fin
        """
        
        # 1. Obtener y validar datos de entrada
        empleado_id = request.data.get('empleado_id')
        fecha_inicio = request.data.get('fecha_inicio')
        fecha_fin = request.data.get('fecha_fin')

        if not all([empleado_id, fecha_inicio, fecha_fin]):
            return Response({"error": "Faltan datos (empleado_id, fecha_inicio, fecha_fin)."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            empleado = Empleado.objects.select_related('puesto').get(id=empleado_id)
        except Empleado.DoesNotExist:
            return Response({"error": "Empleado no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # 2. Obtener el Sueldo Base
        sueldo_base_mensual = empleado.puesto.salario_base_mensual
        
        # 3. Calcular Horas Trabajadas (Simplificado)
        asistencias = Asistencia.objects.filter(
            empleado=empleado,
            hora_entrada_real__date__gte=fecha_inicio,
            hora_entrada_real__date__lte=fecha_fin
        )
        
        # Lógica de cálculo de horas (Ejemplo simplificado: 8 horas por entrada)
        horas_trabajadas = asistencias.count() * 8 # Asumimos 8 horas por registro de entrada
        
        # 4. Obtener Conceptos Maestros (Solo Sueldo Base y un ejemplo de egreso)
        try:
            concepto_sueldo = ConceptoNomina.objects.get(nombre="Sueldo Base")
            concepto_impuesto = ConceptoNomina.objects.get(nombre="Impuesto Fijo") # Asumimos existe
        except ConceptoNomina.DoesNotExist:
             return Response({"error": "Falta configurar Conceptos Nomina maestros (Sueldo Base, Impuesto Fijo)."}, status=status.HTTP_400_BAD_REQUEST)

        # 5. Cálculo (MUY simplificado para el demo)
        
        # Sueldo proporcional (Usamos el total y lo ajustamos a horas/días trabajados)
        sueldo_proporcional = sueldo_base_mensual / Decimal(30) * Decimal(asistencias.count()) # Dias trabajados
        
        # Montos finales
        monto_bruto = sueldo_proporcional 
        monto_impuesto = monto_bruto * Decimal(0.10) # 10% de impuesto
        monto_neto = monto_bruto - monto_impuesto

        # 6. Crear la Liquidación y los Detalles (Transacciones)
        liquidacion = Liquidacion.objects.create(
            empleado=empleado,
            fecha_inicio_periodo=fecha_inicio,
            fecha_fin_periodo=fecha_fin,
            monto_bruto=monto_bruto,
            monto_neto=monto_neto,
            estado='PEND'
        )
        
        # Creación de los DetalleLiquidacion
        DetalleLiquidacion.objects.bulk_create([
            DetalleLiquidacion(
                liquidacion=liquidacion,
                concepto=concepto_sueldo,
                monto=sueldo_proporcional,
                cantidad=asistencias.count()
            ),
            DetalleLiquidacion(
                liquidacion=liquidacion,
                concepto=concepto_impuesto,
                monto=monto_impuesto
            )
        ])

        # 7. Serializar y devolver el resultado
        serializer = self.get_serializer(liquidacion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)