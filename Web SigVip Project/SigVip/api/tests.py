from django.test import TestCase
import datetime
from django.db import models
from datetime import date
from django.utils import timezone
from .models import Paciente, User, TipoExamen, Examen, Receta, Tratamiento, ConsultaMedica
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model

class PacienteTestCase(TestCase):
    """Esta clase define la testsuite para el Paciente."""

    def setUp(self):
        """Definición de variables generales."""
        self.rut = '12767806-5'
        self.nombre = 'Juan'
        self.apellidoP = 'Perez'
        self.apellidoM = 'Perez'
        self.edad = 23
        self.email = 'Juan.Perez@gmail.com'
        self.telefono = 9876856
        self.direccion = 'La Espuela 6789, Penalolen, Peñalolén, Región Metropolitana'
        self.paciente = Paciente(rut=self.rut ,
                                nombre=self.nombre ,
                                apellidoP=self.apellidoP ,
                                apellidoM=self.apellidoM ,
                                edad=self.edad ,
                                email=self.email ,
                                telefono=self.telefono ,
                                direccion=self.direccion)

    def test_creacion_de_paciente(self):
        """Test de creación de un paciente"""
        old_count = Paciente.pacientes.count()
        self.paciente.save()
        new_count = Paciente.pacientes.count()
        self.assertNotEqual(old_count, new_count)

class UserTestCase(TestCase):
    """Esta clase define la testsuite para el Doc"""

    def setUp(self):
        """Definición de variables generales"""

        self.client = Client()

        self.admin_user = get_user_model().objects.create_superuser(
            rut = '7575618-6',
            nombre = 'Felipe',
            apellidoP = 'Moran',
            apellidoM = 'Cúneo',
            especialidad = 'Administrador',
            email = 'Felipe.Moran@sigvip.com',
            password = 'Estaesmicontraseña2020'
        )

        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            rut = '7087558-6',
            nombre = 'Fernando',
            apellidoP = 'Alonso',
            apellidoM = 'Díaz',
            especialidad = 'Pediatra',
            email = 'Fernando.Alonso@sigvip.com',
            password = 'Estaesmicontraseña2020'
        )

        #self.client.force_login(self.admin_user)

    def test_creacion_de_doctor(self):
        """Prueba que los usuarios se listan en el panel de admin"""
        url = reverse('admin:api_user_changelist')
        print(url)

        res = self.client.get(url)

        self.assertContains(res, self.user.rut)
        self.assertContains(res, self.user.nombre)
        self.assertContains(res, self.user.apellidoP)
        self.assertContains(res, self.user.apellidoM)
        self.assertContains(res, self.user.especialidad)
        self.assertContains(res, self.user.email)

class TipoExamen_TestCase(TestCase):
    def setUp(self):
        self.texamen = "Examen prueba"
        self.tipoExamen = TipoExamen(texamen=self.texamen)
    
    def test_creacion_TipoExamen(self):     
        old_count = TipoExamen.objects.count()
        self.tipoExamen.save()
        new_count = TipoExamen.objects.count()
        self.assertNotEqual(old_count, new_count)

class Examen_TestCase(TestCase):
    def setUp(self):
        self.tipoexamen = TipoExamen.objects.create(texamen="Examen prueba")
   
        self.imagen = "C:\\User\\admin\\Desktop\\Craneo_dicom.zip"
        self.informacionmedica = "vista frontal craneo"
        self.fecha = datetime.date.today()
        self.examen = Examen(tipoexamen = self.tipoexamen,
                            imagen = self.imagen,
                            informacionmedica = self.informacionmedica,
                            fecha = self.fecha)

    def test_creacion_Examen(self):     
        old_count = Examen.objects.count()
        self.examen.save()
        new_count = Examen.objects.count()
        self.assertNotEqual(old_count, new_count)

class Receta_TestCase(TestCase):
    def setUp(self):
        self.medicamento = "Almaxol"
        self.descripcion = "Tomar un comprimido cada 12 horas"
        self.receta = Receta(medicamento = self.medicamento,
                            descripcion = self.descripcion)

    def test_creacion_Receta(self):
        old_count = Receta.objects.count()
        self.receta.save()
        new_count = Receta.objects.count()
        self.assertNotEqual(old_count, new_count)

class Tratamiento_TestCase(TestCase):
    def setUp(self):
        self.receta = Receta.objects.create(medicamento="Almaxol")
        self.examen = Examen.objects.create(tipoexamen=TipoExamen.objects.create(texamen="Examen prueba"))
        self.descripcion = "Hacer reposo"
        self.tratamiento = Tratamiento(receta = self.receta,
                                        examen = self.examen,
                                        descripcion = self.descripcion)
    
    def test_creacion_Tratamiento(self):
        old_count = Tratamiento.objects.count()
        self.tratamiento.save()
        new_count = Tratamiento.objects.count()
        self.assertNotEqual(old_count, new_count)

class ConsultaMedica_TestCase(TestCase):
    def setUp(self):
        self.tema = "Dolores de cabeza y perdida de vista"
        self.rut = Paciente.pacientes.create(rut='7575618-6')
        self.doctor = User.objects.create(nombre='Juan')
        self.tratamiento = Tratamiento.objects.create(descripcion= "Hacer reposo")
        self.diagnostico = "Tumor en la base del craneo"
        self.fecha = datetime.date.today()

        self.consultamedica = ConsultaMedica(tema = self.tema,
                                            rut = self.rut,
                                            doctor = self.doctor,
                                            tratamiento = self.tratamiento,
                                            diagnostico = self.diagnostico,
                                            fecha = self.fecha)

    def test_creacion_ConsultaMedica(self):
        old_count = ConsultaMedica.objects.count()
        self.consultamedica.save()
        new_count = ConsultaMedica.objects.count()
        self.assertNotEqual(old_count, new_count)