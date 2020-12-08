from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = {
    ###POST
    url(r'^paciente/$', CreatePacienteView.as_view(), name='create paciente'),
    url(r'^consultamedica/$', CreateConsultaMedicaView.as_view(), name='create consulta medica'),
    url(r'^tratamiento/$', CreateTratamientoView.as_view(), name='create tratamiento'),
    url(r'^receta/$', CreateRecetaView.as_view(), name='create receta'),
    url(r'^examen/$', CreateExamenView.as_view(), name='create examen'),

    #GET/PUT/DELETE
    url(r'^paciente/(?P<pk>[0-9]+)/$', DetailsPacienteView.as_view(), name='details paciente'),
    url(r'^consultamedica/(?P<pk>[0-9]+)/$', DetailsConsultaMedicaView.as_view(), name='details consulta medica'),
}
urlpatterns = format_suffix_patterns(urlpatterns)