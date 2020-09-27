from django.shortcuts import render
from django.views.generic import TemplateView
from .models import ConsultaMedica,Tratamiento,Receta,Examen
from pacientes.models import Paciente
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
####################################### VIEW #######################################
class HomeFichaView(LoginRequiredMixin,TemplateView):
    def get(self,request,**kwargs):
        rut=kwargs["rut"]
        fromdate = request.GET.get("fromdate")
        if fromdate:
            post = ConsultaMedica.fichas.filter(Q(fecha = fromdate) & Q(rut_id=rut)).distinct
        else:
            orden = request.GET.get("orden")
            if orden == 'descendente':
                post = ConsultaMedica.fichas.filter(rut_id=rut).order_by('fecha').distinct
            else:
                post = ConsultaMedica.fichas.filter(rut_id=rut).distinct
        return render(request,'ficha.html',{'fichas':post})

class DetalleConsultaView(LoginRequiredMixin,TemplateView):
    def get(self,request,**kwargs):
        codigo=kwargs["codigo"]
        return render(request,'consulta_detalle.html',{'detalle':ConsultaMedica.fichas.get(id=codigo)})
####################################### CREATE #######################################
class ConsultaCreate(CreateView):
    model = ConsultaMedica
    template_name = './create_ficha.html'
    fields = '__all__'

class TratamientoCreate(CreateView):
    model = Tratamiento
    template_name = './create_tratamiento.html'
    fields = '__all__'

class ExamenCreate(CreateView):
    model = Examen
    template_name = './create_examenes.html'
    fields = '__all__'

class RecetaCreate(CreateView):
    model = Receta
    template_name = './create_receta.html'
    fields = '__all__'
####################################### UPDATE #######################################
class PacienteUpdate(UpdateView):
    model = Paciente
    template_name = './paciente_form.html'
    fields = ['nombre','apellido','edad','email','telefono','direccion']

class ConsultaUpdate(UpdateView):
    model = ConsultaMedica
    template_name = './actualizar_ficha.html'
    fields = ['tema','tratamiento','diagnostico']

class TratamientoUpdate(UpdateView):
    model = Tratamiento
    template_name = './actualizar_tratamiento.html'
    fields = ['receta','examen','descripcion']

class ExamenUpdate(UpdateView):
    model = Examen
    template_name = './actualizar_examen.html'
    fields = '__all__'

class RecetaUpdate(UpdateView):
    model = Receta
    template_name = './actualizar_receta.html'
    fields = '__all__'
####################################### DELETE #######################################
class ConsultaDelete(DeleteView):
    model = ConsultaMedica
    template_name = './consulta_confirm_delete.html'
    success_url = reverse_lazy('paciente')