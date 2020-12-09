from django.shortcuts import render
from django.views.generic import TemplateView
from api.models import Paciente
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic.edit import CreateView,UpdateView
from django.db.models import Q

####################################### VIEW #######################################
class HomePageView(LoginRequiredMixin,TemplateView):
    def get(self,request,**kwargs):
        return render(request,'index.html',context=None)

class HomePacienteView(LoginRequiredMixin,TemplateView):
    def get(self,request,**kwargs):
        queryset = request.GET.get('buscar')
        post = Paciente.pacientes.all()
        try:
            queryset0,queryset1,queryset2 = queryset.split(" ")

            if queryset2:
                post = Paciente.pacientes.filter(
                    ( Q(nombre = queryset0) & Q(apellidoP = queryset1)) & Q(apellidoM = queryset2) ).distinct
        except:
            try:
                queryset0,queryset1 = queryset.split(" ")
                if queryset1:
                    post = Paciente.pacientes.filter(
                        ( Q(nombre = queryset0) & Q(apellidoP = queryset1)) ).distinct
            except:
                if queryset:
                    post = Paciente.pacientes.filter(Q(rut = queryset) | Q(nombre = queryset) | Q(apellidoP = queryset) | Q(apellidoM = queryset)).distinct
        return render(request,'pacientes.html',{'pacientes':post})
####################################### CREATE #######################################
class PacienteCreate(CreateView):
    model = Paciente
    template_name = './paciente_form.html'
    fields = '__all__'