from django.conf.urls import patterns, include, url
from django.conf import settings
from taller import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'taller.views.home', name='home'),
    # url(r'^taller/', include('taller.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', 'administrador.views.ingresar'),
    url(r'^principal/$', 'administrador.views.principal'),
    url(r'^cerrar/$', 'administrador.views.cerrar'),
    url(r'^perfil/$', 'administrador.views.editar_perfil'),
    url(r'^proyectos/$', 'administrador.views.proyectos'),
    url(r'^crear_metodologia/$', 'administrador.views.crear_metodologia'),
    url(r'^editar/(?P<id_proyecto>\d+)$', 'administrador.views.editar_proyecto'),
    url(r'^proyecto/(?P<id_proyecto>\d+)/(?P<rol>\D*)$','administrador.views.proyecto_detalle'),
    url(r'^proyecto_iterar/(?P<id_proyecto>\d+)/(?P<rol>\D*)$','administrador.views.proyecto_iterar'),
    url(r'^crear_proyecto/$', 'administrador.views.crear_proyecto'),
    url(r'^crear_proyecto_equipo/(?P<id_proyecto>\d+)$', 'administrador.views.crear_proyecto_equipo'),
    url(r'^crear_proyecto_sistema/(?P<id_proyecto>\d+)$', 'administrador.views.crear_proyecto_sistema'),
    url(r'^crear_proyecto_sistema_asociar/(?P<id_proyecto>\d+)/(?P<id_asociado>\d+)$', 'administrador.views.crear_proyecto_sistema_asociar'),
    url(r'^crear_proyecto_iteracion/(?P<id_proyecto>\d+)/(?P<iteracion>\d+)$','administrador.views.crear_proyecto_iteracion'),
    url(r'^eliminar_proyecto/(?P<id_proyecto>\d+)$', 'administrador.views.eliminar_proyecto'),
    url(r'^sistema/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_caracteristica>\d+)$', 'administrador.views.sistema'),
    url(r'^delete_caracteristica/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_caracteristica>\d+)$', 'administrador.views.delete_caracteristica'),
    url(r'^requerimientos/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_requerimiento>\d+)$', 'administrador.views.requerimientos'),
    url(r'^eliminar_requerimiento/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_requerimiento>\d+)$', 'administrador.views.eliminar_requerimiento'),
    url(r'^requerimiento_crear/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_requerimiento>\d+)$', 'administrador.views.requerimiento_crear'),
#    url(r'^caracteristica_crear/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_caracteristica>\d+)$', 'administrador.views.caracteristica_crear'),
    url(r'^iteracion/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_iteracion>\d+)$', 'administrador.views.iteracion_detalle'),
    url(r'^requerimientos_detalle/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_requerimiento>\d+)$', 'administrador.views.requerimiento_detalle'),
    url(r'^casos_uso_detalle/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_caso>\d+)$', 'administrador.views.casos_uso_detalle'),
    url(r'^escenarios_crear/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_caso>\d+)$', 'administrador.views.escenarios_crear'),
    url(r'^escenarios_crear2/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_caso>\d+)/(?P<numero_esc>\d+)/(?P<numero_camp>\d+)$', 'administrador.views.escenarios_crear2'),
    url(r'^escenarios_crear3/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_caso>\d+)/(?P<numero_esc>\d+)/(?P<numero_camp>\d+)/(?P<contador>\d+)$', 'administrador.views.escenarios_crear3'),
    url(r'^escenario_detalle/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_caso>\d+)/(?P<id_escenario>\d+)$', 'administrador.views.escenario_detalle'),
    url(r'^eliminar_escenario/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_caso>\d+)/(?P<id_escenario>\d+)$', 'administrador.views.eliminar_escenario'),
    url(r'^caso_prueba_detalle/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_caso>\d+)/(?P<id_casoprueba>\d+)$', 'administrador.views.caso_prueba_detalle'),
    url(r'^caso_prueba_detalle_llenar/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_caso>\d+)/(?P<id_casoprueba>\d+)$', 'administrador.views.caso_prueba_detalle_llenar'),
    url(r'^caso_prueba_detalle_llenar2/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_caso>\d+)/(?P<id_casoprueba>\d+)/(?P<numero_camp>\d+)$', 'administrador.views.caso_prueba_detalle_llenar2'),
    url(r'^caso_prueba_crear/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_caso>\d+)/(?P<id_escenario>\d+)$', 'administrador.views.caso_prueba_crear'),
    url(r'^caso_prueba_crear2/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_caso>\d+)/(?P<id_escenario>\d+)/(?P<numero_cas>\d+)/(?P<numero_camp>\d+)$', 'administrador.views.caso_prueba_crear2'),
    url(r'^caso_prueba_crear3/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_caso>\d+)/(?P<id_escenario>\d+)/(?P<numero_cas>\d+)/(?P<numero_camp>\d+)/(?P<contador>\d+)$', 'administrador.views.caso_prueba_crear3'),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT,}),
    url(r'^casos_uso/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_casouso>\d+)$', 'administrador.views.casos_uso'),
    url(r'^delete_casos_uso/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_casouso>\d+)$', 'administrador.views.delete_casos_uso'),
    url(r'^casos_uso_crear/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)/(?P<id_casouso>\d+)$', 'administrador.views.casos_uso_crear'),
    url(r'^pruebas$', 'administrador.views.pruebas'),
    url(r'^probar/(?P<id_casouso>\d+)$', 'administrador.views.probar'),
    url(r'^gestionar/(?P<id_proyecto>\d+)/(?P<id_sistema>\d+)$', 'administrador.views.gestionar'),
    url(r'^asignarpruebas/(?P<id_proyecto>\d+)$', 'administrador.views.asignarpruebas'),
    url(r'^artefactos/(?P<id_proyecto>\d+)/(?P<rol>\D*)$', 'administrador.views.artefactos'),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),


    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
