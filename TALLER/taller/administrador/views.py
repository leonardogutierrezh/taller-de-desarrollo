from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from administrador.forms import UserForm, ProyectoForm, MiembroForm, ProyectoeForm, RequerimientoForm, IteracionForm, SistemaForm
from administrador.models import Perfil
from administrador.models import Miembro, Proyecto, Requerimiento, Iteracion, Sistema, SistemaAsociado, Caracteristica
from django.core.urlresolvers import reverse

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
            perfiles.usuario = usuario
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
def proyecto_detalle(request,id_proyecto,rol):
    dato = Proyecto.objects.get(pk=id_proyecto)
    sistemas = SistemaAsociado.objects.filter(proyecto=dato)
    iteraciones = Iteracion.objects.filter(proyecto=dato)
    if dato.iteActual > 0:
      iteracion = Iteracion.objects.get(proyecto=dato,numero=dato.iteActual)
      iteracion.status="En progreso"
      return render_to_response('proyecto_detalle.html',{'proyecto':dato,'rol':rol,'iteracion':iteracion,'iteraciones':iteraciones}, context_instance=RequestContext(request))
    else:
      return render_to_response('proyecto_detalle.html',{'proyecto':dato,'rol':rol,'sistemas':sistemas,'iteraciones':iteraciones}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def crear_proyecto(request):
    if request.method=='POST':
        formulario = ProyectoForm(request.POST)
        if formulario.is_valid():
          usuario = request.user
          formulario2 = formulario.save(commit=False)
          formulario2.save()
          instance = Proyecto.objects.get(pk=formulario2.id)
          administrador = Miembro.objects.create(usuario=usuario,proyecto=instance)
          administrador.rol = 'Gerente de Proyecto'
          administrador.save()
          redireccion = '/crear_proyecto_iteracion/' + str(formulario2.id) + '/0'
          return HttpResponseRedirect(redireccion)
    else:
        formulario = ProyectoForm()
    return render_to_response('crear_proyecto.html',{'formulario':formulario}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def crear_proyecto_iteracion(request, id_proyecto,iteracion):
  proyecto = Proyecto.objects.get(pk=id_proyecto)
  iteracionInt = int(iteracion)
  print proyecto.iteraciones
  if proyecto.iteraciones > iteracionInt:
    print "entre"
    if request.method=='POST':
      formulario = IteracionForm(request.POST,request.FILES)
      if formulario.is_valid():
        formulario2 = formulario.save(commit=False)
        iteracionInt = iteracionInt + 1
        formulario2.proyecto = proyecto
        formulario2.numero = iteracionInt
        formulario2.status = "Inactiva"
        formulario2.save()

        redireccion = '/crear_proyecto_iteracion/' + str(id_proyecto) + '/' + str(iteracionInt)
        return HttpResponseRedirect(redireccion)
    else:
      formulario = IteracionForm()
      numero = iteracionInt + 1
    return render_to_response('crear_proyecto_iteracion.html',{'formulario':formulario,'numero':numero}, context_instance=RequestContext(request))
  else:
    redireccion = '/crear_proyecto_sistema/' + str(id_proyecto)
    return HttpResponseRedirect(redireccion)

@login_required(login_url='/') 
def crear_proyecto_sistema(request,id_proyecto):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    sistemas = SistemaAsociado.objects.exclude(proyecto=proyecto)
    sistemasAso = SistemaAsociado.objects.filter(proyecto=proyecto)
    if request.method=='POST':
        formulario = SistemaForm(request.POST)
        if formulario.is_valid():
          formulario2 = formulario.save()
          print formulario2.id
          print formulario2.nombre
          print formulario2.descripcion

          asociado = SistemaAsociado.objects.create(sistema=formulario2,proyecto=proyecto)
          print "se creo asociado"
          print "antes de guardar"
          asociado.save()
          redireccion = '/crear_proyecto_sistema/' + str(id_proyecto)
          return HttpResponseRedirect(redireccion)
    else:
        formulario = SistemaForm()
    return render_to_response('crear_proyecto_sistema.html',{'sistemas':sistemas,'formulario':formulario,'sistemasAso':sistemasAso,'id_proyecto':id_proyecto}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def crear_proyecto_sistema_asociar(request,id_proyecto,id_asociado):
    asociado = SistemaAsociado.objects.get(pk=id_asociado)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    asociadonew = SistemaAsociado.objects.create(sistema=asociado.sistema,proyecto=proyecto)
    asociadonew.save()
    redireccion = '/crear_proyecto_sistema/' + str(id_proyecto)
    return HttpResponseRedirect(redireccion)


@login_required(login_url='/') 
def crear_proyecto_equipo(request,id_proyecto):
    print "entre a crear"
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    miembros = Miembro.objects.filter(proyecto = proyecto)
    redireccion = '/crear_proyecto_equipo/' + str(id_proyecto)
    if request.method=='POST':
        miembro_form = MiembroForm(request.POST)
        print "pase el post"
        if miembro_form.is_valid():
          print "pase 1"
          formulario = miembro_form.save(commit=False)
          print "pase 2"
          formulario.proyecto = proyecto
          print "pase 3"
          formulario.save()
          return HttpResponseRedirect(redireccion)
    else:
        formulario = MiembroForm()
    return render_to_response('crear_proyecto_equipo.html',{'formulario':formulario,'miembros':miembros}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def proyecto_iterar(request,id_proyecto,rol):
  proyecto = Proyecto.objects.get(pk=id_proyecto)
  if proyecto.iteActual < proyecto.iteraciones:
    if proyecto.iteActual != 0:
      iteracion = Iteracion.objects.get(proyecto=proyecto,numero=proyecto.iteActual)
      iteracion.status="Finalizada"
      iteracion.save()
    proyecto.iteActual = proyecto.iteActual + 1 
    iteracionNew = Iteracion.objects.get(proyecto=proyecto,numero=proyecto.iteActual)
    iteracionNew.status="En Proceso"
    iteracionNew.save()
    proyecto.save()
  else:
    iteracion = Iteracion.objects.get(proyecto=proyecto,numero=proyecto.iteActual)
    iteracion.status="Finalizada"
    iteracion.save()
    proyecto.iteActual = -1
    print proyecto.iteActual
    proyecto.save()
  redireccion = '/proyecto/' + str(id_proyecto) + '/' + rol
  return HttpResponseRedirect(redireccion)

@login_required(login_url='/') 
def iteracion_detalle(request,id_proyecto,rol,id_iteracion):
    iteracion= Iteracion.objects.get(pk=id_iteracion)
    return render_to_response('iteracion.html',{'iteracion':iteracion,'id':id_proyecto,'rol':rol}, context_instance=RequestContext(request))
	

@login_required(login_url='/') 
def eliminar_proyecto(request,id_proyecto):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    proyecto.delete()
    return render_to_response('proyecto_eliminado.html')

@login_required(login_url='/') 
def editar_proyecto(request,id_proyecto):
    usuario = request.user
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if request.method == 'POST':
        # formulario enviado
        proyecto_form = ProyectoeForm(request.POST)
        print proyecto_form
        if proyecto_form.is_valid():
            print "valido"
            formulario = proyecto_form.save(commit=False)
            proyecto.fechaInicio = formulario.fechaInicio
            proyecto.fechaFin = formulario.fechaFin
            proyecto.descripcion = formulario.descripcion
            proyecto.metodologia = formulario.metodologia
            proyecto.recursos = formulario.recursos
            proyecto.iteraciones = formulario.iteraciones           
            proyecto.save()
            return render_to_response('proyecto_editado.html')

    else:
        # formulario inicial
        proyecto_form = ProyectoeForm(instance = proyecto)
    return render_to_response('editar_proyecto.html', { 'formulario': proyecto_form, 'usuario': usuario }, context_instance=RequestContext(request))

@login_required(login_url='/') 
def sistema(request,id_proyecto,rol,id_sistema):
    sistema = Sistema.objects.get(pk=id_sistema)
    requerimientos = Caracteristica.objects.filter(sistema=sistema)
    return render_to_response('sistema.html', { 'requerimientos': requerimientos,'sistema':sistema,'id':id_proyecto,'rol':rol }, context_instance=RequestContext(request))

@login_required(login_url='/') 
def crear_requerimiento(request, id_proyecto,rol):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if request.method=='POST':
        formulario_req = RequerimientoForm(request.POST)
        if formulario_req.is_valid():
          requerimiento = formulario_req.save(commit=False)
          requerimiento.proyecto = proyecto
          requerimiento.save()
          redireccion = '/requerimientos/' + str(id_proyecto) + '/' + str(rol)
          return HttpResponseRedirect(redireccion)
    else:
        formulario_req = RequerimientoForm()
    return render_to_response('crear_requerimiento.html',{'formulario_req':formulario_req, 'id': id_proyecto}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def requerimiento_detalle(request,id_proyecto,rol,id_requerimiento):
    dato = Requerimiento.objects.get(pk=id_requerimiento)
    return render_to_response('requerimiento_detalle.html',{'requerimiento':dato,'rol':rol,'id':id_proyecto}, context_instance=RequestContext(request))
