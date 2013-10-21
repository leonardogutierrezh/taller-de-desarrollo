from django.contrib import admin
from administrador.models import Proyecto
from administrador.models import Miembro
from administrador.models import *

class Proyecto_UserInline(admin.TabularInline):
		model = Miembro
		extra = 1

class ProyectoAdmin(admin.ModelAdmin):
		list_display = ('nombre','fechaInicio')
		list_filter = ['fechaInicio']
		search_fields = ['nombre']
		fieldsets = [
        (None,               {'fields': ['nombre']}),
        ('Informacion de Creacion', {'fields': ['fechaInicio','fechaFin','iteraciones','descripcion','metodologia'], 'classes': ['collapse']}),
    ]
		inlines = [Proyecto_UserInline]


admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(Perfil)
admin.site.register(Requerimiento)
admin.site.register(Iteracion)
admin.site.register(Sistema)
admin.site.register(Escenario)
admin.site.register(EscenarioExtra)
admin.site.register(EscenarioValor)
admin.site.register(CasoPrueba)
admin.site.register(Caracteristica)
admin.site.register(EjecucionCasoPrueba)
admin.site.register(CasoPruebaDetalle)
admin.site.register(Miembro)
admin.site.register(Artefactos)

