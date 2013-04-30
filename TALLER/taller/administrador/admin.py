from django.contrib import admin
from administrador.models import Proyecto
from administrador.models import Miembro

class Proyecto_UserInline(admin.TabularInline):
		model = Miembro
		extra = 1

class ProyectoAdmin(admin.ModelAdmin):
		list_display = ('nombre','fecha')
		list_filter = ['fecha']
		search_fields = ['nombre']
		fieldsets = [
        (None,               {'fields': ['nombre']}),
        ('Informacion de Creacion', {'fields': ['fecha','descripcion','metodologia'], 'classes': ['collapse']}),
    ]
		inlines = [Proyecto_UserInline]


admin.site.register(Proyecto, ProyectoAdmin)
