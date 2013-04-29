from django.conf.urls import patterns, url

from administrador import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
