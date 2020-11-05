from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from API import models
from .models import Paciente, ConsultaMedica, Tratamiento, Receta, Examen, TipoExamen

class UserAdmin(BaseUserAdmin):
    """Ordene por id"""
    ordering = ['id']
    """Display por email y nombre"""
    list_display = ['rut','nombre','apellidoP','apellidoM','especialidad','email']

    fieldsets = (
        (None,
            {'fields':('email','password')}
        ),

        (_('Personal Info'),
            {'fields': ('rut','nombre','apellidoP','apellidoM','especialidad')}
        ),

        (_('Permissions'), 
            {'fields': ('is_active', 'is_staff','is_superuser')}
        ),

        (_('Important Dates'),
            {'fields': ('last_login',)}
        )
    )

    add_fieldsets = (
        (None,{
            'classes': ('wide',),
            'fields': ('rut','nombre','apellidoP','apellidoM','especialidad','email','password1','password2')
        }),
    )

admin.site.register(models.User, UserAdmin)
admin.site.register(Paciente)
admin.site.register(ConsultaMedica)
admin.site.register(Tratamiento)
admin.site.register(Receta)
admin.site.register(Examen)
admin.site.register(TipoExamen)