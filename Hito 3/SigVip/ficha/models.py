from django.db import models
from datetime import date
from pacientes.models import Paciente
from django.contrib.auth.models import User

class TipoExamen(models.Model):
    texamen = models.CharField(max_length=45,unique=True)

    def __str__(self):
        return "{}".format(self.texamen)

class Examen(models.Model):
    tipoexamen = models.ForeignKey(TipoExamen,default=None,on_delete=models.CASCADE)
    imagen = models.CharField(max_length=45)
    informacionmedica = models.CharField(max_length=500)
    fecha = models.DateField(default=date.today)

    def __str__(self):
        return "{}".format(self.tipoexamen)

class Receta(models.Model):
    medicamento = models.CharField(max_length=60,unique=True)
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return "{}".format(self.medicamento)

class Tratamiento(models.Model):
    receta = models.ForeignKey(Receta,default=None,on_delete=models.CASCADE)
    examen = models.ForeignKey(Examen,default=None,on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return "{}".format(self.descripcion)

class ConsultaMedica(models.Model):
    tema = models.CharField(max_length=100)
    rut = models.ForeignKey(Paciente,default=None,on_delete=models.CASCADE)
    doctor = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    tratamiento = models.ForeignKey(Tratamiento,default=None,on_delete=models.CASCADE)
    diagnostico = models.CharField(max_length=200)
    fecha = models.DateField(default=date.today)
    fichas = models.Manager()

    def __str__(self):
        return "{}".format(self.tema)
