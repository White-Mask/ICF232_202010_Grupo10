from rest_framework import serializers
from .models import Paciente, ConsultaMedica, Tratamiento, Receta, Examen

class PacienteSerializer(serializers.ModelSerializer):
    """Serializador para mapear un paciente a formato JSON"""

    class Meta:
        """Meta clase para el mapeo de atributos"""
        model = Paciente
        fields = '__all__'
        read_only_fields = ()

class ConsultaMedicaSerializer(serializers.ModelSerializer):
    """Serializador para mapear un ConsultaMedica a formato JSON"""

    class Meta:
        """Meta clase para el mapeo de atributos"""
        model = ConsultaMedica
        fields = '__all__'
        read_only_fields = ()

class TratamientoSerializer(serializers.ModelSerializer):
    """Serializador para mapear un Tratamiento a formato JSON"""

    class Meta:
        """Meta clase para el mapeo de atributos"""
        model = Tratamiento
        fields = '__all__'
        read_only_fields = ()

class RecetaSerializer(serializers.ModelSerializer):
    """Serializador para mapear un Receta a formato JSON"""

    class Meta:
        """Meta clase para el mapeo de atributos"""
        model = Receta
        fields = '__all__'
        read_only_fields = ()

class ExamenSerializer(serializers.ModelSerializer):
    """Serializador para mapear un Examen a formato JSON"""

    class Meta:
        """Meta clase para el mapeo de atributos"""
        model = Examen
        fields = '__all__'
        read_only_fields = ()