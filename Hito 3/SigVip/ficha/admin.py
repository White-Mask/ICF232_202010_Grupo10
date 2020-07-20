from django.contrib import admin
from .models import *

admin.site.register(ConsultaMedica)
admin.site.register(Tratamiento)
admin.site.register(Receta)
admin.site.register(Examen)
admin.site.register(TipoExamen)