from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from administrador.forms import UserForm, ProyectoForm, MiembroForm, ProyectoeForm, RequerimientoForm, IteracionForm, SistemaForm, CaracteristicaForm, CasosDeUsoForm, EscenarioDefineForm, EscenarioExtraForm, EscenarioForm, EscenarioValorForm, CasoPruebaForm, CasoPruebaExtraForm, CasoPruebaValorForm, CasoPruebaDefineForm, CasoPruebaDetalleDefineForm, CasoPruebaDetalleForm, MetodologiaForm, EjecucionCasoPruebaForm,ProbarForm, ArtefactosForm
from administrador.models import Perfil
from administrador.models import *
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
import datetime

def ingresar(request):
  if request.method == 'POST':
    formulario = AuthenticationForm(request.POST)
    print "hola"
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
  casos = CasoPruebaDetalle.objects.filter(probador=usuario, desicion="Por ejecutar").count()
  proy_miembros = Miembro.objects.filter(usuario=usuario)
  metodologias = Metodologia.objects.all().count()
  info  = []
  proys = []
  for p in proy_miembros:
    if p.proyecto in proys:
      continue
    proys.append(p.proyecto)
    
  for p in proys:
    sistemas = SistemaAsociado.objects.filter(proyecto=p)
    _dict = {}
    _dict["proyecto"]=p
    _dict["sistemas"]=sistemas
    proy_miembros = Miembro.objects.filter(proyecto=p)
    _dict["roles"]=map(lambda x:x.rol,proy_miembros)
    

    info.append(_dict)
    
  return render_to_response('principal.html',{'casos': casos,  'info': info,'usuario':usuario, 'metodologias':metodologias}, context_instance=RequestContext(request))

@login_required(login_url='/')
def cerrar(request):
  logout(request)
  return HttpResponseRedirect('/')

@login_required(login_url='/') 
def editar_perfil(request):
    metodologias = Metodologia.objects.all().count()
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
    return render_to_response('perfil.html', {'metodologias': metodologias, 'user_form': user_form, 'usuario': usuario }, context_instance=RequestContext(request))

@login_required(login_url='/') 
def crear_metodologia(request):
    metodologias = Metodologia.objects.all().count()
    if request.method=='POST':
      formulario = MetodologiaForm(request.POST)
      if formulario.is_valid():
	usuario = request.user
	metodologia = formulario.save(commit=False)
	metodologia.usuario = usuario
	metodologia.save()
	
    usuario = request.user
    formulario = MetodologiaForm()
    return render_to_response('crear_metodologia.html', {'metodologias':metodologias, 'formulario': formulario, 'usuario': usuario }, context_instance=RequestContext(request))
    #return render_to_response('crear_metodologia.html', { 'usuario': usuario }, context_instance=RequestContext(request))

@login_required(login_url='/') 
def proyectos(request):
    usuario = request.user
    metodologias = Metodologia.objects.all().count()
    proyectos = Miembro.objects.filter(usuario=usuario)
    return render_to_response('proyectos.html', {'metodologias':metodologias, 'proyectos': proyectos, 'usuario': usuario }, context_instance=RequestContext(request))

@login_required(login_url='/') 
def proyecto_detalle(request,id_proyecto,rol):
    dato = Proyecto.objects.get(pk=id_proyecto)
    sistemas = SistemaAsociado.objects.filter(proyecto=dato)
    iteraciones = Iteracion.objects.filter(proyecto=dato)
    artefactos = Artefactos.objects.filter(proyecto=dato)
    if dato.iteActual > 0:
      iteracion = Iteracion.objects.get(proyecto=dato,numero=dato.iteActual)
      iteracion.status="En progreso"
      return render_to_response('proyecto_detalle.html',{'proyecto':dato,'rol':rol,'iteracion':iteracion,'iteraciones':iteraciones,'sistemas':sistemas}, context_instance=RequestContext(request))
    else:
      return render_to_response('proyecto_detalle.html',{'artefactos':artefactos, 'proyecto':dato,'rol':rol,'sistemas':sistemas,'iteraciones':iteraciones}, context_instance=RequestContext(request))

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
            rol = miembro_form.cleaned_data.get('rol')
	    privilegio = 10

            for k in rol:
                if k == 'Gerente de Proyecto' and privilegio > 1 :
                    privilegio = 1
                    rol_aux = k
  		if k == 'Gerente de Pruebas' and privilegio > 2 :
                    privilegio = 2
                    rol_aux = k
  		if k == 'Analista de Pruebas' and privilegio > 3 :
                    privilegio = 3
                    rol_aux = k
  		if k == 'Disenador de Pruebas' and privilegio > 4 :
                    privilegio = 4
                    rol_aux = k
  		if k == 'Cliente' and privilegio > 5 :
                    privilegio = 5
                    rol_aux = k
  		if k == 'Probador' and privilegio > 6 :
                    privilegio = 6
                    rol_aux = k
  		if k == 'Analista de Requerimiento' and privilegio > 7 :
                    privilegio = 7
                    rol_aux = k
			
            formulario = Miembro.objects.create(usuario=miembro_form.cleaned_data.get('usuario'), proyecto = proyecto, rol=rol_aux, privilegio=privilegio)
            formulario.save()
            print formulario.privilegio
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
def sistema(request,id_proyecto,rol,id_sistema,id_caracteristica):
    sistema = Sistema.objects.get(pk=id_sistema)
    caracteristica = Caracteristica.objects.filter(sistema=sistema)
    caracteristicas = Caracteristica.objects.all().count()
    sistema = Sistema.objects.get(pk=id_sistema)
    if request.method=='POST':
      carac = request.POST.getlist('caracteristica')
      prese = request.POST.getlist('presedencia')
      prioridad = request.POST.getlist('prioridad')
      i = 0
      while i < len(carac):
        try:        
          if prese[i] == 'null':
            value = None
          else:
            value = Caracteristica.objects.get(pk=prese[i])
          Caracteristica.objects.create(nombre=carac[i],precedencia=value,prioridad=prioridad[i],sistema=sistema,detalle=False)
          i += 1
        except:         
          i += 1
    if id_caracteristica != '0':
      dato = Caracteristica.objects.get(pk=id_caracteristica)
    return render_to_response('sistema.html', { 'caracteristica': caracteristica, 'caracteristicas': caracteristicas, 'sistema':sistema,'id':id_proyecto,'rol':rol }, context_instance=RequestContext(request))

@login_required(login_url='/') 
def delete_caracteristica(request,id_proyecto,rol,id_sistema,id_caracteristica):
    sistema = Sistema.objects.get(pk=id_sistema)
    caracteristica = Caracteristica.objects.get(pk=id_caracteristica).delete()
    redireccion = '/sistema/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/0'
    return HttpResponseRedirect(redireccion)   

@login_required(login_url='/') 
def requerimientos(request,id_proyecto,rol,id_sistema,id_requerimiento):
    #requerimiento = Sistema.objects.get(pk=id_sistema)
    dato =""
    sistema= Sistema.objects.get(pk=id_sistema)
    requerimientos = Requerimiento.objects.filter(sistema=sistema)
    caracteristica = Caracteristica.objects.filter(sistema=sistema)
    if request.method=='POST':
      ids = request.POST.getlist('id')
      nombre = request.POST.getlist('nombre')
      carac = request.POST.getlist('caracteristica')
      i = 0
      while i < len(ids):
        try:
          value = Caracteristica.objects.get(pk=carac[i])
          Requerimiento.objects.create(nombre=nombre[i],caracteristica=value,idrequerimiento=ids[i],sistema=sistema,detalle=False)
          i += 1
        except:         
          i += 1
    if id_requerimiento != '0':
      dato = Requerimiento.objects.get(pk=id_requerimiento)
      if dato.detalle == False:
        redireccion = '/requerimiento_crear/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_requerimiento)
        return HttpResponseRedirect(redireccion)   
    return render_to_response('requerimientos.html', {'dato':dato,'caracteristica':caracteristica,'requerimientos': requerimientos,'sistema':sistema,'id':id_proyecto,'rol':rol }, context_instance=RequestContext(request))

@login_required(login_url='/') 
def requerimiento_crear(request,id_proyecto,rol,id_sistema,id_requerimiento):
    if request.method=='POST':
        formulario = RequerimientoForm(request.POST,request.FILES)
        if formulario.is_valid():
          req = Requerimiento.objects.get(pk=id_requerimiento)
          requerimiento = formulario.save(commit=False)
          if requerimiento.imagen == None:
              requerimiento.imagen = None  
          print "victoria"
          sistema= Sistema.objects.get(pk=id_sistema)
          req.sistema = sistema
          req.descripcion = requerimiento.descripcion
          req.imagen = requerimiento.imagen
          req.prioridad = requerimiento.prioridad
          req.interfaz = requerimiento.interfaz
          req.reglas = requerimiento.reglas
          req.detalle = True
          req.save()
          redireccion = '/requerimientos/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/0'
          return HttpResponseRedirect(redireccion)
    else:
        formulario = RequerimientoForm()
    return render_to_response('crear_requerimiento.html',{'formulario':formulario, 'id': id_proyecto,'rol':rol,'id_sistema':id_sistema}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def requerimiento_detalle(request,id_proyecto,rol,id_sistema,id_requerimiento):
    dato = Requerimiento.objects.get(pk=id_requerimiento)
    return render_to_response('requerimiento_detalle.html',{'requerimiento':dato,'rol':rol,'id':id_proyecto,'id_sistema':id_sistema}, context_instance=RequestContext(request))
    
@login_required(login_url='/') 
def casos_uso(request,id_proyecto,rol,id_sistema,id_casouso):
    dato = ""
    sistema = Sistema.objects.get(pk=id_sistema)
    caracteristicas = Caracteristica.objects.all().count()
    casos = CasosDeUso.objects.filter(sistema=sistema)
    valores = []
    orden = []
    if request.method=='POST':
      caso = request.POST.getlist('caso')
      actor = request.POST.getlist('actor')
      i = 0
      while i < len(caso):
        try:        
          CasosDeUso.objects.create(caso=caso[i],actor=actor[i],sistema=sistema,detalle=False)
          i += 1
        except:         
          i += 1    
    if id_casouso != '0':
      dato = CasosDeUso.objects.get(pk=id_casouso)
      if dato.detalle==False:
        redireccion = '/casos_uso_crear/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_casouso)
        return HttpResponseRedirect(redireccion)   
    return render_to_response('casos_uso.html', {'dato':dato, 'casos': casos,'sistema':sistema, 'caracteristicas':caracteristicas, 'id':id_proyecto,'rol':rol }, context_instance=RequestContext(request))

@login_required(login_url='/') 
def delete_casos_uso(request,id_proyecto,rol,id_sistema,id_casouso):
    caso = CasosDeUso.objects.get(pk=id_casouso).delete()
    redireccion = '/casos_uso/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/0'
    return HttpResponseRedirect(redireccion)   

@login_required(login_url='/') 
def casos_uso_crear(request,id_proyecto,rol,id_sistema,id_casouso):
    if request.method=='POST':
        formulario = CasosDeUsoForm(request.POST)
        if formulario.is_valid():
          dato = CasosDeUso.objects.get(pk=id_casouso)
          caso = formulario.save(commit=False)
          dato.requerimiento = caso.requerimiento
          dato.descripcion = caso.descripcion
          dato.detalle = True
          dato.precondicion = caso.precondicion
          dato.save()
          redireccion = '/casos_uso/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/0'
          return HttpResponseRedirect(redireccion)
    else:
        formulario = CasosDeUsoForm()
    return render_to_response('crear_casos_uso.html',{'formulario':formulario, 'id': id_proyecto,'rol':rol,'id_sistema':id_sistema}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def casos_uso_detalle(request,id_proyecto,rol,id_sistema,id_caso):
    dato = CasosDeUso.objects.get(pk=id_caso)
    sistema = Sistema.objects.get(pk=id_sistema)
    titulos = EscenarioExtra.objects.filter(sistema=sistema)
    escenarios = Escenario.objects.filter(caso=dato)
    valores = []
    orden = []
    if request.method=='POST':
      print "entreeeeeeeeeeeeeeeeeeeeeeeeeeee"
      num = request.POST.getlist('numero')
      ori = request.POST.getlist('originario')
      alt = request.POST.getlist('alterno')
      listaTitulos = []
      for titulo in titulos:
        elemento = request.POST.getlist(titulo.titulo)
        print elemento
        tupla = titulo, elemento
        listaTitulos.append(tupla)
      i = 0
      while i < len(num):
        try:        
          esc = Escenario.objects.create(caso=dato,numero=num[i],flujoOriginario=ori[i],flujoAlterno=alt[i])
          for elem in listaTitulos:
            if elem[0].activo:
              EscenarioValor.objects.create(escenario=esc,titulo=elem[0],valor=elem[1][i])
          i += 1
        except:         
          print "hizo except"
          i += 1
    for escenario in escenarios:
        for titulo in titulos:
            try:
              orden.append(EscenarioValor.objects.get(escenario=escenario,titulo=titulo))
            except:
              orden.append("N/A")
        valores.append(orden)
        orden = []
    lista = zip(escenarios,valores)    
    return render_to_response('casos_uso_detalle.html', {'lista':lista, 'titulos':titulos, 'caso':dato, 'rol':rol, 'id':id_proyecto, 'id_sistema':id_sistema, 'id_caso':id_caso}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def escenarios_crear(request,id_proyecto,rol,id_sistema,id_caso):
    sistema = Sistema.objects.get(pk=id_sistema)
    titulos = EscenarioExtra.objects.filter(sistema=sistema)
    if request.method == 'POST':
      eliminar = request.POST.getlist("titulos")
      lista = request.POST.getlist("alist")
      print "la longitud " + str(len(eliminar))
      for item in eliminar:
        print "un item"
        desactivar = EscenarioExtra.objects.get(id=item)
        desactivar.activo = False
        desactivar.save()
      for item in lista:
        EscenarioExtra.objects.create(sistema=sistema, titulo=item, activo=True)
      redireccion = '/casos_uso_detalle/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_caso)
      return HttpResponseRedirect(redireccion)
    else:
        formulario = EscenarioDefineForm()
    return render_to_response('crear_escenario.html', {'titulos': titulos, 'formulario': formulario, 'id': id_proyecto, 'rol': rol, 'id_sistema': id_sistema}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def escenarios_crear2(request,id_proyecto,rol,id_sistema,id_caso,numero_esc,numero_camp):
    extra=int(numero_camp)
    formularioSet = formset_factory(EscenarioExtraForm,extra=extra,can_delete=True)
    if request.method=='POST':
        formulario = formularioSet(request.POST)
        if formulario.is_valid():
          for form in formulario:
            titulo = form.save(commit=False)
            sistema= Sistema.objects.get(pk=id_sistema)
            titulo.sistema = sistema
            titulo.save()
          redireccion = '/casos_uso_detalle/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_caso)
          return HttpResponseRedirect(redireccion)
    else:
        if numero_camp=='0':  
            redireccion = '/casos_uso_detalle/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_caso)
            return HttpResponseRedirect(redireccion)
        else:
            formulario = formularioSet
            return render_to_response('crear_escenario2.html',{'formulario':formulario, 'id': id_proyecto,'rol':rol,'id_sistema':id_sistema}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def escenarios_crear3(request,id_proyecto,rol,id_sistema,id_caso,numero_esc,numero_camp,contador):
    cont = int(contador)
    num_esc = int(numero_esc)
    if cont < num_esc:
      sistema= Sistema.objects.get(pk=id_sistema)
      caso = CasosDeUso.objects.get(pk=id_caso)
      escenarios = Escenario.objects.filter(caso=caso)
      titulos = EscenarioExtra.objects.filter(sistema=sistema)
      extra=len(titulos) 
      camposSet = formset_factory(EscenarioValorForm,extra=extra)
      if request.method=='POST':
          formulario = camposSet(request.POST)
          escenario= EscenarioForm(request.POST)
          if formulario.is_valid() and escenario.is_valid():
            cont = cont + 1
            lista= zip(formulario,titulos) 
            esc = escenario.save(commit=False)
            esc.caso = caso
            esc.numero = 1 + len(escenarios)
            esc.save()
            print "empieza" 
            for l in lista:
              elemento = l[0].save(commit=False)
              elemento.titulo= l[1]
              elemento.escenario = esc
              elemento.save()
            print "termina"
            redireccion = '/escenarios_crear3/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_caso) + '/' + str(numero_esc) + '/' + str(numero_camp) + '/' + str(cont)
            return HttpResponseRedirect(redireccion)
      else:
          cont = cont + 1
          campos = camposSet
          formulario = EscenarioForm()
          return render_to_response('crear_escenario3.html',{'formulario':formulario,'campos':campos,'titulos':titulos, 'id': id_proyecto,'rol':rol,'id_sistema':id_sistema,'contador':cont}, context_instance=RequestContext(request))
    else:
      redireccion = '/casos_uso_detalle/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_caso)
      return HttpResponseRedirect(redireccion)

@login_required(login_url='/') 
def caso_prueba_crear(request,id_proyecto,rol,id_sistema,id_caso,id_escenario):
    sistema = Sistema.objects.get(pk=id_sistema)
    titulos = CasoPruebaExtra.objects.filter(sistema=sistema)
    escenario = Escenario.objects.get(pk=id_escenario)
    if request.method=='POST':
      eliminar = request.POST.getlist("titulos")
      lista = request.POST.getlist("alist")
      print "la longitud " + str(len(eliminar))
      for item in eliminar:
        print "un item"
        desactivar = CasoPruebaExtra.objects.get(id=item)
        desactivar.activo = False
        desactivar.save()
      for item in lista:
        CasoPruebaExtra.objects.create(sistema=sistema,titulo=item,activo=True)
      redireccion = '/escenario_detalle/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_caso) + '/' + str(id_escenario)
      return HttpResponseRedirect(redireccion)
    else:
        formulario = CasoPruebaDefineForm()
    return render_to_response('crear_casoprueba.html',{'titulos':titulos,'formulario':formulario, 'id': id_proyecto,'rol':rol,'id_sistema':id_sistema,'escenario':escenario}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def caso_prueba_crear2(request,id_proyecto,rol,id_sistema,id_caso,id_escenario,numero_cas,numero_camp):
    extra=int(numero_camp)
    formularioSet = formset_factory(CasoPruebaExtraForm,extra=extra,can_delete=True)
    if request.method=='POST':
        formulario = formularioSet(request.POST)
        if formulario.is_valid():
          for form in formulario:
            titulo = form.save(commit=False)
            sistema= Sistema.objects.get(pk=id_sistema)
            titulo.sistema = sistema
            titulo.save()
            redireccion = '/caso_prueba_crear3/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_caso) + '/' + str(id_escenario) + '/' + str(numero_cas) + '/' + str(numero_camp)  + '/0'
          return HttpResponseRedirect(redireccion)
    else:
        if numero_camp=='0':  
            redireccion = '/caso_prueba_crear3/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_caso) + '/' + str(id_escenario) + '/' + str(numero_cas) + '/' + str(numero_camp)  + '/0'
            return HttpResponseRedirect(redireccion)
        else:
            formulario = formularioSet
            return render_to_response('crear_casoprueba2.html',{'formulario':formulario, 'id': id_proyecto,'rol':rol,'id_sistema':id_sistema}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def caso_prueba_crear3(request,id_proyecto,rol,id_sistema,id_caso,id_escenario,numero_cas,numero_camp,contador):
    cont = int(contador)
    num_cas = int(numero_cas)
    if cont < num_cas:
      sistema= Sistema.objects.get(pk=id_sistema)
      caso = Escenario.objects.get(pk=id_escenario)
      escenarios = Escenario.objects.filter(caso=caso)
      titulos = CasoPruebaExtra.objects.filter(sistema=sistema)
      extra=len(titulos) 
      camposSet = formset_factory(CasoPruebaValorForm,extra=extra)
      if request.method=='POST':
          formulario = camposSet(request.POST)
          casoPrueba= CasoPruebaForm(request.POST)
          if formulario.is_valid() and casoPrueba.is_valid():
            cont = cont + 1
            lista= zip(formulario,titulos) 
            cas = casoPrueba.save(commit=False)
            cas.escenario = caso
            cas.detalle = False
            cas.save()
            print "empieza" 
            for l in lista:
              elemento = l[0].save(commit=False)
              elemento.titulo= l[1]
              elemento.caso = cas
              elemento.save()
            print "termina"
            redireccion = '/caso_prueba_crear3/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_caso) + '/' + str(id_escenario) + '/' + str(numero_cas) + '/' + str(numero_camp)  + '/' + str(cont)
            return HttpResponseRedirect(redireccion)
      else:
          cont = cont + 1
          campos = camposSet
          formulario = CasoPruebaForm()
          return render_to_response('crear_casoprueba3.html',{'formulario':formulario,'campos':campos,'titulos':titulos, 'id': id_proyecto,'rol':rol,'id_sistema':id_sistema,'contador':cont}, context_instance=RequestContext(request))
    else:
      redireccion = '/casos_uso_detalle/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_caso)
      return HttpResponseRedirect(redireccion)

@login_required(login_url='/') 
def escenario_detalle(request,id_proyecto,rol,id_sistema,id_caso,id_escenario):
    dato = Escenario.objects.get(pk=id_escenario)
    sistema = Sistema.objects.get(pk=id_sistema)
    titulos = CasoPruebaExtra.objects.filter(sistema=sistema)
    casos = CasoPrueba.objects.filter(escenario=dato)
    valores = []
    orden = []
    if request.method=='POST':
      ids = request.POST.getlist('id')
      nombres = request.POST.getlist('nombre')
      esperados = request.POST.getlist('esperado')
      niveles = request.POST.getlist('nivel')
      tipos = request.POST.getlist('tipo')
      listaTitulos = []
      for titulo in titulos:
        print titulo.titulo
        elemento = request.POST.getlist(titulo.titulo)
        print "el elemento"
        print elemento
        tupla = titulo, elemento
        listaTitulos.append(tupla)
      print "el largo de la lista de titulos" + str(len(listaTitulos))
      i = 0
      while i < len(ids):
        try:        
          cas = CasoPrueba.objects.create(escenario=dato,idcaso=ids[i],nombre=nombres[i],resultado=esperados[i],nivel=niveles[i],tipo=tipos[i],detalle=False)
          for elem in listaTitulos:
            print "antes del elemento"
            if elem[0].activo:
              CasoPruebaValor.objects.create(caso=cas,titulo=elem[0],valor=elem[1][i])
          i += 1
        except:         
          i += 1
    for caso in casos:
        print len(titulos)
        for titulo in titulos:
            try:
              orden.append(CasoPruebaValor.objects.get(caso=caso,titulo=titulo))
            except:
              orden.append("N/A")
        valores.append(orden)
        orden = []
    lista = zip(casos,valores)    
    return render_to_response('escenario_detalle.html',{'lista':lista,'titulos':titulos,'escenario':dato,'rol':rol,'id':id_proyecto,'id_sistema':id_sistema,'id_caso':id_caso,'id_escenario':id_escenario}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def caso_prueba_detalle(request,id_proyecto,rol,id_sistema,id_caso,id_casoprueba):
    dato = CasoPrueba.objects.get(pk=id_casoprueba)
    escenario = dato.escenario
    if request.method=='POST':
      ids = request.POST.getlist('id')
      nombres = request.POST.getlist('nombre')
      esperados = request.POST.getlist('esperado')
      niveles = request.POST.getlist('nivel')
      tipos = request.POST.getlist('tipo')
      i = 0
      while i < len(ids):
        try:        
          CasoPrueba.objects.create(escenario=escenario,idcaso=ids[i],nombre=nombres[i],resultado=esperados[i],nivel=niveles[i],tipo=tipos[i],detalle=False)
          i += 1
        except:         
          i += 1
    if dato.detalle==False:
      redireccion = '/caso_prueba_detalle_llenar/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_caso) + '/' + str(id_casoprueba)
      return HttpResponseRedirect(redireccion)   
    detalle = CasoPruebaDetalle.objects.get(casoprueba=dato)
    ejecuciones = EjecucionCasoPrueba.objects.filter(caso=dato)
    casos = CasoPrueba.objects.filter(escenario=dato.escenario)
    sistema = Sistema.objects.get(pk=id_sistema)
    titulos = CasoPruebaExtra.objects.filter(sistema=sistema)
    valores = []
    orden = []
    for caso in casos:
      for titulo in titulos:
        try:
          orden.append(CasoPruebaValor.objects.get(caso=caso,titulo=titulo))
        except:
          orden.append("N/A")
      valores.append(orden)
      orden = []
    lista = zip(casos,valores)   
    return render_to_response('escenario_detalle.html',{'ejecuciones':ejecuciones, 'lista': lista, 'titulos': titulos, 'detalle': detalle, 'escenario': escenario, 'rol': rol, 'id': id_proyecto, 'id_sistema': id_sistema, 'id_caso':id_caso, 'id_escenario': escenario.id, 'casoprueba':dato}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def caso_prueba_detalle_llenar(request,id_proyecto,rol,id_sistema,id_caso,id_casoprueba):
    if request.method=='POST':
        formulario = CasoPruebaDetalleForm(request.POST)
        print "entro"
        if formulario.is_valid():
          print "valido"
          casoprueba = CasoPrueba.objects.get(id=id_casoprueba)
          form = formulario.save(commit=False)
          form.casoprueba = casoprueba
          form.sistema = Sistema.objects.get(id=id_sistema)
          form.casouso = CasosDeUso.objects.get(id=id_caso)
          form.autorcaso = request.user
          form.fecha = formulario.cleaned_data['fecha']
          form.save()
          casoprueba.detalle = True
          casoprueba.save()
          pasos = request.POST.getlist('paso')
          condiciones = request.POST.getlist('condicion')
          valores = request.POST.getlist('valor')
          esperados = request.POST.getlist('esperado')
          obtenidos = request.POST.getlist('obtenido')
          i = 0
          while i < len(pasos):
              ejecucion = EjecucionCasoPrueba.objects.create(caso=casoprueba, paso=pasos[i], condicion=condiciones[i], valor= valores[i], resultadoesp=esperados[i], resultadoobt=obtenidos[i])
              ejecucion.save()
              i += 1
          redireccion = '/escenario_detalle/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_caso) + '/' + str(casoprueba.escenario.id)
          return HttpResponseRedirect(redireccion)
    else:
      formulario = CasoPruebaDetalleForm()
    return render_to_response('crear_casopruebadetalle.html',{'formulario':formulario, 'id': id_proyecto,'rol':rol,'id_sistema':id_sistema}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def caso_prueba_detalle_llenar2(request,id_proyecto,rol,id_sistema,id_caso,id_casoprueba,numero_camp):
    sistema= Sistema.objects.get(pk=id_sistema)
#    caso = Escenario.objects.get(pk=id_escenario)
#    escenarios = Escenario.objects.filter(caso=caso)
    titulos = CasoPruebaExtra.objects.filter(sistema=sistema)
    extra= int(numero_camp)
    camposSet = formset_factory(EjecucionCasoPruebaForm,extra=extra)
    if request.method=='POST':
        formulario = camposSet(request.POST)
        casoPrueba= CasoPruebaDetalleForm(request.POST)
        if formulario.is_valid() and casoPrueba.is_valid():
          cont = cont + 1
          lista= zip(formulario,titulos) 
          cas = casoPrueba.save(commit=False)
          cas.escenario = caso
          cas.detalle = False
          cas.save()
          print "empieza" 
          for l in lista:
            elemento = l[0].save(commit=False)
            elemento.titulo= l[1]
            elemento.caso = cas
            elemento.save()
          print "termina"
 #         redireccion = '/caso_prueba_crear3/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_caso) + '/' + str(id_escenario) + '/' + str(numero_cas) + '/' + str(numero_camp)  + '/' + str(cont)
  #        return HttpResponseRedirect(redireccion)
    else:
          campos = camposSet
          formulario = CasoPruebaDetalleForm()
          return render_to_response('crear_casopruebadetalle.html',{'formulario':formulario,'campos':campos,'id': id_proyecto,'rol':rol,'id_sistema':id_sistema}, context_instance=RequestContext(request))

@login_required(login_url='/')
def eliminar_requerimiento(request, id_proyecto, rol, id_sistema, id_requerimiento):
    Requerimiento.objects.get(pk=id_requerimiento).delete()
    return HttpResponseRedirect('/requerimientos' + '/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/0')

@login_required(login_url='/')
def pruebas(request):
  usuario = request.user
  casos = CasoPruebaDetalle.objects.filter(probador=usuario, desicion="Por ejecutar")
  return render_to_response('pruebas.html', {'casos': casos}, context_instance=RequestContext(request))

@login_required(login_url='/')
def probar(request, id_casouso):
  usuario = request.user
  caso = CasoPrueba.objects.get(pk=id_casouso)
  caso_detalle = CasoPruebaDetalle.objects.get(casoprueba=caso)
  ejecuciones = EjecucionCasoPrueba.objects.filter(caso=caso)
  if caso_detalle.probador == usuario:
    if request.method == 'POST':
        formulario = ProbarForm(request.POST)
        if formulario.is_valid():
          caso_detalle.fechaejec = formulario.cleaned_data['fecha']
          if formulario.cleaned_data['aprobado'] == 'Aprobo':
            caso_detalle.fechaapro = datetime.date.today()
          caso_detalle.desicion = formulario.cleaned_data['aprobado']
          caso_detalle.notas = formulario.cleaned_data['notas']
          caso_detalle.save()
          for ejecucion in ejecuciones:
            print ejecucion.id
            if request.POST.get(str(ejecucion.id)) == None:
              continue
            else:
              ejecucion.resultadoobt = request.POST.get(str(ejecucion.id))
              print ejecucion.resultadoobt
              ejecucion.save()
          return HttpResponseRedirect('/pruebas')
    else:
      formulario = ProbarForm(initial={'fecha': caso_detalle.fechaejec, 'notas': caso_detalle.notas})
    return render_to_response('probar.html', {'ejecuciones': ejecuciones, 'formulario': formulario, 'caso': caso, 'detalle': caso_detalle}, context_instance=RequestContext(request))
  return HttpResponseRedirect('/')

@login_required(login_url='/')
def gestionar(request, id_proyecto):
  proyecto = Proyecto.objects.get(pk=id_proyecto)
  pruebas_aprob = CasoPruebaDetalle.objects.filter(desicion="Aprobo")
  pruebas_fallo = CasoPruebaDetalle.objects.filter(desicion="Fallo")
  pruebas_ejecutar = CasoPruebaDetalle.objects.filter(desicion="Por ejecutar")
  return render_to_response('gestionar.html', {'proyecto':proyecto, "aprobadas": pruebas_aprob, 'fallas': pruebas_fallo, "ejecutar": pruebas_ejecutar}, context_instance=RequestContext(request))

@login_required(login_url='/')
def asignarpruebas(request, id_proyecto):
  proyecto = Proyecto.objects.get(pk=id_proyecto)
  pruebas_ejecutar = CasoPruebaDetalle.objects.filter(desicion="Por ejecutar")
  probadores = Miembro.objects.filter(proyecto=proyecto, rol='Probador')
  if request.method == 'POST':
    nuevos = request.POST.getlist('probador')
    for item in nuevos:
      if item == 'None':
        continue
      else:
        div = item.split('_')
        case = CasoPruebaDetalle.objects.get(pk=div[0])
        prob = User.objects.get(pk=div[1])
        case.probador = prob
        case.save()
        print div
  return render_to_response('asignarpruebas.html', {"proyecto": proyecto, 'ejecutar': pruebas_ejecutar, 'probadores': probadores}, context_instance=RequestContext(request))

@login_required(login_url='/')
def artefactos(request, id_proyecto,rol):
  usuario = request.user
  proyecto = Proyecto.objects.get(pk=id_proyecto)
  if request.method == 'POST':
    formulario = ArtefactosForm(request.POST,request.FILES)
    if formulario.is_valid():
      form = formulario.save(commit=False)
      form.proyecto = proyecto
      form.save()
      return HttpResponseRedirect("/proyecto/" + str(id_proyecto) + "/" + rol )
  else:
    formulario = ArtefactosForm()
  return render_to_response('artefactos.html',{'formulario': formulario},context_instance=RequestContext(request))

@login_required(login_url='/')
def eliminar_escenario(request, id_proyecto, rol, id_sistema, id_caso, id_escenario):
    Escenario.objects.get(pk=id_escenario).delete()
    return HttpResponseRedirect('/casos_uso_detalle' + '/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + id_caso)
