from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = {
    ###CREATE
    url(r'^paciente/$', CreatePacienteView.as_view(), name='create paciente'),
    url(r'^consultamedica/$', CreateConsultaMedicaView.as_view(), name='create consulta medica'),
    url(r'^tratamiento/$', CreateTratamientoView.as_view(), name='create tratamiento'),
    url(r'^receta/$', CreateRecetaView.as_view(), name='create receta'),
    url(r'^examen/$', CreateExamenView.as_view(), name='create examen')

}
urlpatterns = format_suffix_patterns(urlpatterns)