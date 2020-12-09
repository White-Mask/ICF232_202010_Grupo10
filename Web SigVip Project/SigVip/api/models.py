from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from api.Validacion_de_Run import verificador_run

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        """Crear un nuevo usuario con email y password"""
        if not email:
            raise ValueError('Se debe especificar un correo valido')
        
        user = self.model(email=self.normalize_email(email),**extra_fields)

        """"Permisos"""
        user.is_staff = True

        """Password encriptada"""
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Crear un superusuario con email y password"""
        superuser = self.create_user(email, password, **extra_fields)

        """"Permisos"""
        superuser.is_superuser = True

        """Password encriptada"""
        superuser.set_password(password)
        superuser.save(using=self._db)
        
        return superuser

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)

class User(AbstractBaseUser,PermissionsMixin):
    """Modelo personalizado de usuario"""
    rut = models.CharField(max_length=10,unique=True,validators=[verificador_run])
    nombre = models.CharField(max_length=45)
    apellidoP = models.CharField(max_length=45)
    apellidoM = models.CharField(max_length=45)
    especialidad = models.CharField(max_length=45)
    email = models.EmailField(max_length=60,unique=True)
    
    """Permisos de usuario"""
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['rut','nombre', 'apellidoP','apellidoM']

class Paciente(models.Model):
    rut = models.CharField(max_length=10,unique=True,validators=[verificador_run])
    nombre = models.CharField(max_length=45)
    apellidoP = models.CharField(max_length=45)
    apellidoM = models.CharField(max_length=45)
    edad = models.IntegerField()
    email = models.EmailField(max_length=60)
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=200)
    pacientes = models.Manager()

    def __str__(self):
        return "{}".format(self.rut)

class TipoExamen(models.Model):
    texamen = models.CharField(max_length=45,unique=True)

    def __str__(self):
        return "{}".format(self.texamen)

class Examen(models.Model):
    tipoexamen = models.ForeignKey(TipoExamen,default=None,on_delete=models.CASCADE)
    imagen = models.FileField(default=None, blank=True)
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