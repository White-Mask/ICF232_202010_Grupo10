from django.shortcuts import render
from django.views.generic import TemplateView
from .models import ConsultaMedica,Tratamiento,Receta
from pacientes.models import Paciente
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

class HomeFichaView(LoginRequiredMixin,TemplateView):
    def get(self,request,**kwargs):
        rut=kwargs["rut"]
        return render(request,'ficha.html',{'fichas':ConsultaMedica.fichas.filter(rut_id=rut)})

class DetalleConsultaView(LoginRequiredMixin,TemplateView):
    def get(self,request,**kwargs):
        codigo=kwargs["codigo"]
        return render(request,'consulta_detalle.html',{'detalle':ConsultaMedica.fichas.get(id=codigo)})

class ConsultaCreate(CreateView):
    model = ConsultaMedica
    template_name = './actualizar_form.html'
    fields = '__all__'

class TratamientoCreate(CreateView):
    model = Tratamiento
    template_name = './tratamiento_form.html'
    fields = '__all__'

class RecetaCreate(CreateView):
    model = Receta
    template_name = './receta_form.html'
    fields = '__all__'

class ConsultaUpdate(UpdateView,):
    model = ConsultaMedica
    template_name = './actualizar_form.html'
    fields = ['tema','tratamiento','diagnostico']

class PacienteUpdate(UpdateView):
    model = Paciente
    template_name = './paciente_form.html'
    fields = ['nombre','apellido','edad','email','telefono','direccion']

class TratamientoUpdate(UpdateView):
    model = Tratamiento
    template_name = './tratamiento_form.html'
    fields = ['receta','examen','descripcion']
        

class ConsultaDelete(DeleteView):
    model = ConsultaMedica
    template_name = './consulta_confirm_delete.html'
    success_url = reverse_lazy('paciente')