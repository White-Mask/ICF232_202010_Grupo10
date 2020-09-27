from django.conf.urls import url,re_path
from django.urls import path,include
from . import views

urlpatterns = [
    ###CREATE
    url(r'^(?P<fk>\d+)/create/$',views.ConsultaCreate.as_view(success_url='pacientes/'),name='consulta_create'),
    re_path(r'^(?P<fk>\d+)/create/create_tratamiento/$',views.TratamientoCreate.as_view(success_url='pacientes/'),name='tratamiento_create'),
    re_path(r'^(?P<fk>\d+)/create/create_tratamiento/create_examen/$',views.ExamenCreate.as_view(success_url='pacientes/'),name='examen_create'),
    re_path(r'^(?P<fk>\d+)/create/create_tratamiento/create_receta/$',views.RecetaCreate.as_view(success_url='pacientes/'),name='receta_create'),
    ###VIEW
    re_path(r'^(?P<rut>\d+)/$',views.HomeFichaView.as_view(),name='fichas'),
    re_path(r'^(?P<fk>\d+)/detalle/(?P<codigo>\d+)/?$',views.DetalleConsultaView.as_view(),name='detalle'),
    ###UPDATE
    url(r'^(?P<pk>\d+)/update/$',views.PacienteUpdate.as_view(success_url='pacientes/'),name='paciente_update'),
    re_path(r'^(?P<fk>\d+)/detalle/(?P<pk>\d+)/?update/$',views.ConsultaUpdate.as_view(success_url='pacientes/'),name='consulta_update'),
    re_path(r'^(?P<fk>\d+)/detalle/(?P<codigo>\d+)/update/(?P<pk>\d+)/?$',views.TratamientoUpdate.as_view(success_url='pacientes/'),name='tratamiento_update'),
    re_path(r'^(?P<fk>\d+)/detalle/(?P<codigo>(\d+))/update/(?P<tratamiento_id>(\d+))/(?P<pk>\d+)/?$',views.ExamenUpdate.as_view(success_url='pacientes/'),name='examen_update'),
    re_path(r'^(?P<fk>\d+)/detalle/(?P<codigo>(\d+))/update/(?P<tratamiento_id>(\d+))/(?P<pk>\d+)/?$',views.RecetaUpdate.as_view(success_url='pacientes/'),name='receta_update'),
    ###DELETE
    re_path(r'^(?P<fk>\d+)/detalle/(?P<pk>(\d+))/?delete/$',views.ConsultaDelete.as_view(success_url='pacientes/'),name='consulta_delete'),
]