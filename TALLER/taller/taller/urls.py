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
    url(r'^crear_proyecto/$', 'administrador.views.crear_proyecto'),
    url(r'^crear_proyecto/(?P<id_proyecto>\d+)$', 'administrador.views.crear_proyecto_equipo'),
    url(r'^eliminar_proyecto/(?P<id_proyecto>\d+)$', 'administrador.views.eliminar_proyecto'),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
