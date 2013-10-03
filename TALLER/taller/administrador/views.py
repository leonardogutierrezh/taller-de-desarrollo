from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from administrador.forms import UserForm, ProyectoForm, MiembroForm, ProyectoeForm, RequerimientoForm, IteracionForm, SistemaForm, CaracteristicaForm, CasosDeUsoForm, EscenarioDefineForm, EscenarioExtraForm, EscenarioForm, EscenarioValorForm, CasoPruebaForm, CasoPruebaExtraForm, CasoPruebaValorForm, CasoPruebaDefineForm, CasoPruebaDetalleDefineForm, CasoPruebaDetalleForm, EjecucionCasoPruebaForm
from administrador.models import Perfil
from administrador.models import Miembro, Proyecto, Requerimiento, Iteracion, Sistema, SistemaAsociado, Caracteristica, CasosDeUso, Escenario, EscenarioExtra, EscenarioValor, CasoPrueba, CasoPruebaExtra, CasoPruebaValor
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory 

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
      return render_to_response('proyecto_detalle.html',{'proyecto':dato,'rol':rol,'iteracion':iteracion,'iteraciones':iteraciones,'sistemas':sistemas}, context_instance=RequestContext(request))
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
def sistema(request,id_proyecto,rol,id_sistema):
    sistema = Sistema.objects.get(pk=id_sistema)
    caracteristica = Caracteristica.objects.filter(sistema=sistema)
    return render_to_response('sistema.html', { 'caracteristica': caracteristica,'sistema':sistema,'id':id_proyecto,'rol':rol }, context_instance=RequestContext(request))

@login_required(login_url='/') 
def requerimientos(request,id_proyecto,rol,id_sistema):
    #requerimiento = Sistema.objects.get(pk=id_sistema)
    sistema= Sistema.objects.get(pk=id_sistema)
    requerimientos = Requerimiento.objects.filter(sistema=sistema)
    return render_to_response('requerimientos.html', { 'requerimientos': requerimientos,'sistema':sistema,'id':id_proyecto,'rol':rol }, context_instance=RequestContext(request))

@login_required(login_url='/') 
def caracteristica_crear(request,id_proyecto,rol,id_sistema):
    if request.method=='POST':
        formulario = CaracteristicaForm(request.POST)
        if formulario.is_valid():
          caracteristica = formulario.save(commit=False)
          if caracteristica.precedencia == None:
              caracteristica.precedencia = None  
          print "victoria"
          sistema= Sistema.objects.get(pk=id_sistema)
          caracteristica.sistema = sistema
          caracteristica.save()
          redireccion = '/sistema/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema)
          return HttpResponseRedirect(redireccion)
    else:
        formulario = CaracteristicaForm()
    return render_to_response('crear_caracteristica.html',{'formulario':formulario, 'id': id_proyecto,'rol':rol,'id_sistema':id_sistema}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def requerimiento_crear(request,id_proyecto,rol,id_sistema):
    if request.method=='POST':
        formulario = RequerimientoForm(request.POST,request.FILES)
        if formulario.is_valid():
          requerimiento = formulario.save(commit=False)
          if requerimiento.imagen == None:
              requerimiento.imagen = None  
          print "victoria"
          sistema= Sistema.objects.get(pk=id_sistema)
          requerimiento.sistema = sistema
          requerimiento.save()
          redireccion = '/requerimientos/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema)
          return HttpResponseRedirect(redireccion)
    else:
        formulario = RequerimientoForm()
    return render_to_response('crear_requerimiento.html',{'formulario':formulario, 'id': id_proyecto,'rol':rol,'id_sistema':id_sistema}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def requerimiento_detalle(request,id_proyecto,rol,id_sistema,id_requerimiento):
    dato = Requerimiento.objects.get(pk=id_requerimiento)
    return render_to_response('requerimiento_detalle.html',{'requerimiento':dato,'rol':rol,'id':id_proyecto,'id_sistema':id_sistema}, context_instance=RequestContext(request))
    
@login_required(login_url='/') 
def casos_uso(request,id_proyecto,rol,id_sistema):
    sistema = Sistema.objects.get(pk=id_sistema)
    casos = CasosDeUso.objects.filter(sistema=sistema)
    return render_to_response('casos_uso.html', { 'casos': casos,'sistema':sistema,'id':id_proyecto,'rol':rol }, context_instance=RequestContext(request))

@login_required(login_url='/') 
def casos_uso_crear(request,id_proyecto,rol,id_sistema):
    if request.method=='POST':
        formulario = CasosDeUsoForm(request.POST)
        if formulario.is_valid():
          caso = formulario.save(commit=False)
          sistema= Sistema.objects.get(pk=id_sistema)
          caso.sistema = sistema
          caso.save()
          redireccion = '/casos_uso/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema)
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
    for escenario in escenarios:
        for titulo in titulos:
            orden.append(EscenarioValor.objects.get(escenario=escenario,titulo=titulo))
        valores.append(orden)
        orden = []
    lista = zip(escenarios,valores)    
    return render_to_response('casos_uso_detalle.html',{'lista':lista,'titulos':titulos,'caso':dato,'rol':rol,'id':id_proyecto,'id_sistema':id_sistema,'id_caso':id_caso}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def escenarios_crear(request,id_proyecto,rol,id_sistema,id_caso):
    if request.method=='POST':
        formulario = EscenarioDefineForm(request.POST)
        if formulario.is_valid():
          numeroEsc = formulario.cleaned_data['numeroEscenarios']
          numeroCamp = formulario.cleaned_data['numeroCampos']
          redireccion = '/escenarios_crear2/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_caso) + '/' + str(numeroEsc) + '/' + str(numeroCamp)
          return HttpResponseRedirect(redireccion)
    else:
        formulario = EscenarioDefineForm()
    return render_to_response('crear_escenario.html',{'formulario':formulario, 'id': id_proyecto,'rol':rol,'id_sistema':id_sistema}, context_instance=RequestContext(request))

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
            print sistema.nombre
            titulo.sistema = sistema
            titulo.save()
          redireccion = '/escenarios_crear3/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_caso) + '/' + str(numero_esc) + '/' + str(numero_camp)  + '/0'
          return HttpResponseRedirect(redireccion)
    else:
        if numero_camp=='0':  
            redireccion = '/escenarios_crear3/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_caso) + '/' + str(numero_esc) + '/' + str(numero_camp) + '/0'
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
    if request.method=='POST':
        formulario = CasoPruebaDefineForm(request.POST)
        if formulario.is_valid():
          numeroCas = formulario.cleaned_data['numeroCasos']
          numeroCamp = formulario.cleaned_data['numeroCampos']
          redireccion = '/caso_prueba_crear2/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_caso) + '/' + str(id_escenario) + '/'+ str(numeroCas) + '/' + str(numeroCamp)
          return HttpResponseRedirect(redireccion)
    else:
        formulario = CasoPruebaDefineForm()
    return render_to_response('crear_casoprueba.html',{'formulario':formulario, 'id': id_proyecto,'rol':rol,'id_sistema':id_sistema}, context_instance=RequestContext(request))

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
      i = 0
      while i < len(ids):
        try:        
          CasoPrueba.objects.create(escenario=dato,idcaso=ids[i],nombre=nombres[i],resultado=esperados[i],nivel=niveles[i],tipo=tipos[i],detalle=False)
          i += 1
        except:         
          i += 1
    for caso in casos:
        for titulo in titulos:
            orden.append(CasoPruebaValor.objects.get(caso=caso,titulo=titulo))
        valores.append(orden)
        orden = []
    lista = zip(casos,valores)    
    return render_to_response('escenario_detalle.html',{'lista':lista,'titulos':titulos,'escenario':dato,'rol':rol,'id':id_proyecto,'id_sistema':id_sistema,'id_caso':id_caso,'id_escenario':id_escenario}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def caso_prueba_detalle(request,id_proyecto,rol,id_sistema,id_caso,id_casoprueba):
    dato = CasoPrueba.objects.get(pk=id_casoprueba)
    if dato.detalle==False:
      redireccion = '/caso_prueba_detalle_llenar/' + str(id_proyecto) + '/' + str(rol) + '/' + str(id_sistema) + '/' + str(id_caso) + '/' + str(id_casoprueba)
      return HttpResponseRedirect(redireccion)      
    return render_to_response('escenario_detalle.html',{'lista':lista,'titulos':titulos,'escenario':dato,'rol':rol,'id':id_proyecto,'id_sistema':id_sistema,'id_caso':id_caso,'id_escenario':id_escenario}, context_instance=RequestContext(request))

@login_required(login_url='/') 
def caso_prueba_detalle_llenar(request,id_proyecto,rol,id_sistema,id_caso,id_casoprueba):
    if request.method=='POST':
        formulario = CasoPruebaDetalleForm(request.POST)
        if formulario.is_valid():
          casoprueba = CasoPrueba.objects.get(id=id_casoprueba)
          form = formulario.save(commit=False)
          form.casoprueba = casoprueba
          form.sistema = Sistema.objects.get(id=id_sistema)
          form.casouso = CasosDeUso.objects.get(id=id_caso)
          form.save()
          casoprueba.detalle = True
          return HttpResponseRedirect(redireccion)
    else:
      formulario = CasoPruebaDetalleForm()
    return render_to_response('crear_casoprueba.html',{'formulario':formulario, 'id': id_proyecto,'rol':rol,'id_sistema':id_sistema}, context_instance=RequestContext(request))

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
          print "ajaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
          formulario = CasoPruebaDetalleForm()
          return render_to_response('crear_casopruebadetalle.html',{'formulario':formulario,'campos':campos,'id': id_proyecto,'rol':rol,'id_sistema':id_sistema}, context_instance=RequestContext(request))
