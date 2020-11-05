from django.test import TestCase, Client

# Create your tests here.
from .models import User, Paciente
from django.contrib.auth import get_user_model
from django.urls import reverse

class UserTestCase(TestCase):
    """Esta clase define la testsuite para el Doc"""

    def setUp(self):
        """Definición de variables generales"""

        self.client = Client()

        self.admin_user = get_user_model().objects.create_superuser(
            rut = '157786357',
            nombre = 'Felipe',
            apellido = 'Moran',
            especialidad = 'Administrador',
            email = 'Felipe.moran@gmail.com',
            password = 'Estaesmicontraseña2020'
        )

        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            rut = '187786357',
            nombre = 'Pedro',
            apellido = 'Jackson',
            especialidad = 'Pediatra',
            email = 'pedro.jackson@gmail.com',
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
        self.assertContains(res, self.user.apellido)
        self.assertContains(res, self.user.especialidad)
        self.assertContains(res, self.user.email)
        

class PacienteTestCase(TestCase):
    """Esta clase define la testsuite para el Paciente"""

    def setUp(self):
        """Definición de variables generales"""
        self.rut = '190083764'
        self.nombre = 'Victor'
        self.apellido = 'Ortuza'
        self.edad = 27
        self.email = 'Vicx@hotmail.com'
        self.telefono = '9875643'
        self.direccion = 'Antonio Varas, 8000'
        self.paciente = Paciente.pacientes.create(rut=self.rut, nombre=self.nombre, apellido=self.apellido, edad=self.edad, email=self.email, telefono=self.telefono, direccion=self.direccion)

    def test_creacion_de_paciente(self):
        """Test de creacion de un paciente"""
        print(Paciente)
        print(self.assertEqual(Paciente.pacientes.count(), 1))
        self.assertEqual(Paciente.pacientes.count(), 1)