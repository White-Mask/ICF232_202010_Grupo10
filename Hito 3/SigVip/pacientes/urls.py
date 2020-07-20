from django.conf.urls import url
from django.urls import path,include
from pacientes import views

urlpatterns = [
    url(r'^$',views.HomePageView.as_view() ,name="index"),
    url(r'pacientes/',views.HomePacienteView.as_view() ,name="paciente"),
    url(r'^paciente/create/$',views.PacienteCreate.as_view(success_url='pacientes/'),name='paciente_create'),
    path('ficha/',include('ficha.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
]