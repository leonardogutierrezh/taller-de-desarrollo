from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from administrador.forms import UserForm, ProyectoForm, MiembroForm
from administrador.models import Perfil
from administrador.models import Miembro, Proyecto

def ingresar(request):
  if request.method == 'POST':
    formulario = AuthenticationForm(request.POST)
    if formulario.is_valid:
      usuario = request.POST['username']
      clave = request.POST['password']
      acceso = authenticate(username=usuario, password=clave)
      if acceso is not None:
        if acceso.is_active:
          login(request,acceso)
          return HttpResponseRedirect('/principal')
        else:
          return render_to_response('noactivo.html', context_instance=RequestContext(request))
      else:
        return render_to_response('nousuario.html', context_instance=RequestContext(request))
  else:
    formulario = AuthenticationForm()
  return render_to_response('ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))

@login_required(login_url='/')
def principal(request):
  usuario = request.user
  return render_to_response('principal.html',{'usuario':usuario}, context_instance=RequestContext(request))

@login_required(login_url='/')
def cerrar(request):
  logout(request)
  return HttpResponseRedirect('/')

@login_required(login_url='/') 
def editar_perfil(request):
    usuario = request.user
    if Perfil.objects.filter(pk=usuario.id):
        perfiles = Perfil.objects.get(pk=usuario.id)
    else:
        perfiles = Perfil.objects.create(usuario=usuario)
    if request.method == 'POST':
        # formulario enviado
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            formulario = user_form.save(commit=False)
            perfiles.direccion = formulario.direccion
            perfiles.telefono = formulario.telefono
            perfiles.cargo = formulario.cargo
            # formulario validado correctamente
            perfiles.save()
            return HttpResponseRedirect('/principal')

    else:
        # formulario inicial
        user_form = UserForm(instance = perfiles)
    return render_to_response('perfil.html', { 'user_form': user_form, 'usuario': usuario }, context_instance=RequestContext(request))

@login_required(login_url='/') 
def proyectos(request):
    usuario = request.user
    proyectos = Miembro.objects.filter(usuario=usuario)
    return render_to_response('proyectos.html', { 'proyectos': proyectos, 'usuario': usuario }, context_instance=RequestContext(request))

@login_required(login_url='/') 
def proyecto_detalle(request,id_proyecto):
    print id_proyecto
    dato = Proyecto.objects.get(pk=id_proyecto)
    return render_to_response('proyecto_detalle.html',{'proyecto':dato}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def crear_proyecto(request):
    if request.method=='POST':
        formulario = ProyectoForm(request.POST)
        if formulario.is_valid():
          formulario.save()
          return HttpResponseRedirect('/proyectos')
    else:
        formulario = ProyectoForm()
    return render_to_response('crear_proyecto.html',{'formulario':formulario}, context_instance=RequestContext(request))
