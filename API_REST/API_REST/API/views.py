from django.shortcuts import render

from rest_framework import generics
from .serializers import *
from .models import Paciente, ConsultaMedica, Tratamiento, Receta, Examen

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response

class CreatePacienteView(generics.ListCreateAPIView):
    """Vista que representa el comportamiento de la API REST
    El queryset contiene la coleccion con todos los Pacientes"""

    queryset = Paciente.pacientes.all()
    serializer_class = PacienteSerializer

    def perform_create(self, serializer):
        """Almacena los datos recibidos mediante POST"""
        serializer.save()

class CreateConsultaMedicaView(generics.ListCreateAPIView):
    """Vista que representa el comportamiento de la API REST
    El queryset contiene la coleccion con todos los ConsultaMedica"""

    queryset = ConsultaMedica.fichas.all()
    serializer_class = ConsultaMedicaSerializer

    def perform_create(self, serializer):
        """Almacena los datos recibidos mediante POST"""
        serializer.save()

class CreateTratamientoView(generics.ListCreateAPIView):
    """Vista que representa el comportamiento de la API REST
    El queryset contiene la coleccion con todos los Tratamiento"""

    queryset = Tratamiento.objects.all()
    serializer_class = TratamientoSerializer

    def perform_create(self, serializer):
        """Almacena los datos recibidos mediante POST"""
        serializer.save()

class CreateRecetaView(generics.ListCreateAPIView):
    """Vista que representa el comportamiento de la API REST
    El queryset contiene la coleccion con todos los Receta"""

    queryset = Receta.objects.all()
    serializer_class = RecetaSerializer

    def perform_create(self, serializer):
        """Almacena los datos recibidos mediante POST"""
        serializer.save()

class CreateExamenView(generics.ListCreateAPIView):
    """Vista que representa el comportamiento de la API REST
    El queryset contiene la coleccion con todos los Examen"""

    queryset = Examen.objects.all()
    serializer_class = ExamenSerializer

    def perform_create(self, serializer):
        """Almacena los datos recibidos mediante POST"""
        serializer.save()