from django.conf.urls import patterns, include, url
from django.conf import settings

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
    url(r'^editar/(?P<id_proyecto>\d+)$', 'administrador.views.editar_proyecto'),
    url(r'^proyecto/(?P<id_proyecto>\d+)/(?P<rol>\D*)$','administrador.views.proyecto_detalle'),
    url(r'^proyecto_iterar/(?P<id_proyecto>\d+)/(?P<rol>\D*)$','administrador.views.proyecto_iterar'),
    url(r'^crear_proyecto/$', 'administrador.views.crear_proyecto'),
    url(r'^crear_proyecto_equipo/(?P<id_proyecto>\d+)$', 'administrador.views.crear_proyecto_equipo'),
    url(r'^crear_proyecto_sistema/(?P<id_proyecto>\d+)$', 'administrador.views.crear_proyecto_sistema'),
    url(r'^crear_proyecto_sistema_asociar/(?P<id_proyecto>\d+)/(?P<id_asociado>\d+)$', 'administrador.views.crear_proyecto_sistema_asociar'),
    url(r'^crear_proyecto_iteracion/(?P<id_proyecto>\d+)/(?P<iteracion>\d+)$','administrador.views.crear_proyecto_iteracion'),
    url(r'^eliminar_proyecto/(?P<id_proyecto>\d+)$', 'administrador.views.eliminar_proyecto'),
    url(r'^crear_requerimiento/(?P<id_proyecto>\d+)/(?P<rol>\D*)$', 'administrador.views.crear_requerimiento'),
    url(r'^sistema/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)$', 'administrador.views.sistema'),
    url(r'^requerimientos/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)$', 'administrador.views.requerimientos'),
    url(r'^requerimiento_crear/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)$', 'administrador.views.requerimiento_crear'),
    url(r'^caracteristica_crear/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_sistema>\d+)$', 'administrador.views.caracteristica_crear'),
    url(r'^iteracion/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_iteracion>\d+)$', 'administrador.views.iteracion_detalle'),
    url(r'^requerimientos/(?P<id_proyecto>\d+)/(?P<rol>\D*)/(?P<id_requerimiento>\d+)$', 'administrador.views.requerimiento_detalle'),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
