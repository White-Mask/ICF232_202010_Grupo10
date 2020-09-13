from django.db import models
from django.contrib.auth.models import User

class Paciente(models.Model):
    rut = models.CharField(max_length=9, unique=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    edad = models.IntegerField()
    email = models.EmailField(max_length=60)
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=200)
    pacientes = models.Manager()

    def __str__(self):
        return "{}".format(self.rut)

class Doctor(models.Model):
    rut = models.CharField(max_length=9,unique=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    especialidad = models.CharField(max_length=45)
    email = models.EmailField(max_length=60,unique=True)

    usuario = models.ForeignKey(User,default=None,on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.nombre)