#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

class Proyecto(models.Model):
  nombre = models.CharField(max_length=100, unique=True)
  fechaInicio = models.DateField(verbose_name='Fecha de Inicio')
  fechaFin = models.DateField(verbose_name='Fecha de Finalización')
  descripcion = models.TextField(max_length=200, verbose_name='Descripción')
  metodologia = models.ForeignKey('Metodologia', verbose_name='Metodología')
  recursos = models.TextField(max_length=200, verbose_name='Recursos')
  iteraciones = models.IntegerField(verbose_name='Iteraciones')
  iteActual = models.IntegerField(default=0)

class Metodologia(models.Model):
  
  cicloV_types = (
                 ('iteraciones','iteraciones'),
                 ('sprint','sprint'),
                 ('fases','fases'),
                 ('etapas','etapas'),
                 ('entregables','entregables')
                 )

  complementada_types = (
                 ('RUP','RUP'),
                 ('UP','UP'),
                 ('OpenUP','OpenUp'),
                 ('AUP','AUP'),
                 ('SCRUM','SCRUM')
                 )
                 
  usuario = models.ForeignKey(User)
  nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
  siglas = models.CharField(max_length=10, unique=True, verbose_name='Siglas')
  descripcion = models.TextField(max_length=200, verbose_name='Descripción')
  artefactos = models.TextField(max_length=400, verbose_name='Artefactos')
  roles = models.TextField(max_length=400)
  cicloVida = models.CharField(max_length=50,choices=cicloV_types, verbose_name='Ciclo de Vida' )
  divCicloVida = models.IntegerField(verbose_name='División Ciclo Vida')
  complementada = models.CharField(max_length=50, choices=complementada_types, verbose_name='Se complementa con')
  
  def __unicode__(self):
    return self.nombre
  
class Iteracion(models.Model):
  proyecto = models.ForeignKey(Proyecto)
  numero = models.IntegerField()
  objetivo = models.TextField(max_length=100)
  criterio = models.TextField(max_length=100, verbose_name='criterio de evaluación')
  planIteracion = models.FileField(upload_to='planIteracion', verbose_name='Plan de Iteracion')
  planEvaIteracion = models.FileField(upload_to='planEvaIteracion', verbose_name='Plan de evaluación de iteración')
  status = models.CharField(max_length=20)
       
class Miembro(models.Model):
  usuario = models.ForeignKey(User)
  proyecto = models.ForeignKey(Proyecto)
  rol = models.CharField(max_length=400)
  privilegio = models.IntegerField(null=True)

  def __unicode__(self):
    return self.rol

class Perfil(models.Model):
  usuario = models.OneToOneField(User, unique=True)
  telefono = models.CharField(max_length=15, null=True)
  direccion = models.CharField(max_length=100, null=True)
  cargo = models.CharField(max_length=100, null=True)
 # imagen = models.ImageField(upload_to='perfiles',verbose_name='Imágen')

class Sistema(models.Model):
  nombre = models.CharField(max_length=30, unique=True)
  descripcion = models.CharField(max_length=100)

class SistemaAsociado(models.Model):
  sistema = models.ForeignKey(Sistema)
  proyecto = models.ForeignKey(Proyecto)

class Caracteristica(models.Model):
  sistema = models.ForeignKey(Sistema)
  nombre = models.CharField(max_length=40)
  precedencia = models.ForeignKey('self',null=True,blank=True)
  prioridad = models.CharField(max_length=40)
  detalle = models.BooleanField()

  def __unicode__(self):
    return self.nombre

class Requerimiento(models.Model):
  idrequerimiento = models.CharField(max_length=20, verbose_name='ID requerimiento')
  nombre = models.CharField(max_length=30, verbose_name='Nombre del requerimiento')
  sistema = models.ForeignKey(Sistema)
  caracteristica = models.ForeignKey(Caracteristica,verbose_name='Caracteristica Asociada')
  descripcion = models.TextField(max_length=200)
  prioridad =models.CharField(max_length=30)
  interfaz = models.TextField(max_length=200,verbose_name='Interfaz grafica')
  imagen = models.ImageField(upload_to='interfaz',verbose_name='Imagen de interfaz grafica (Opcional)',null=True,blank=True)
  reglas = models.TextField(max_length=200,verbose_name='Reglas del Negocio asociada')
  detalle = models.BooleanField()

  def __unicode__(self):
    return self.nombre

class CasosDeUso(models.Model):
  caso= models.CharField(max_length=50)
  sistema= models.ForeignKey(Sistema)
  requerimiento = models.ForeignKey(Requerimiento,null=True,blank=True)
  actor = models.CharField(max_length=50)
  descripcion = models.TextField(max_length=200)
  precondicion = models.TextField(max_length=200)
  detalle = models.BooleanField()

  def __unicode__(self):
    return self.caso


class Escenario(models.Model):
  caso = models.ForeignKey(CasosDeUso)
  numero= models.TextField(max_length=10,verbose_name='ID Escenario')
  flujoOriginario= models.TextField(max_length=400,verbose_name='Flujo Originario')
  flujoAlterno= models.TextField(max_length=400,verbose_name='Flujo Alterno')

class EscenarioExtra(models.Model):
  sistema = models.ForeignKey(Sistema)
  titulo = models.CharField(max_length=40, verbose_name='Nombre del campo')
  activo = models.BooleanField(default=True)

class EscenarioValor(models.Model):
  escenario = models.ForeignKey(Escenario)
  titulo = models.ForeignKey(EscenarioExtra)
  valor = models.TextField(max_length=400)

class CasoPrueba(models.Model):
  escenario = models.ForeignKey(Escenario)
  idcaso = models.CharField(max_length=40,verbose_name='Id del Caso')
  nombre = models.CharField(max_length=40,verbose_name='Nombre')
  resultado = models.TextField(max_length=400,verbose_name='Resultado Esperado')
  nivel = models.CharField(max_length=40,verbose_name='Nivel de Prueba')
  tipo= models.TextField(max_length=10,verbose_name='Tipo de Prueba')
  detalle = models.BooleanField()

class CasoPruebaExtra(models.Model):
  sistema= models.ForeignKey(Sistema)
  titulo= models.CharField(max_length=40,verbose_name='Nombre del campo')
  activo = models.BooleanField(default=True)

class CasoPruebaValor(models.Model):
  caso = models.ForeignKey(CasoPrueba)
  titulo = models.ForeignKey(CasoPruebaExtra)
  valor = models.TextField(max_length=400)

class CasoPruebaDetalle(models.Model):
  casoprueba = models.ForeignKey(CasoPrueba)
  sistema = models.ForeignKey(Sistema)
  casouso = models.ForeignKey(CasosDeUso)
  requerimiento = models.ForeignKey(Requerimiento,null=True,blank=True)
  version = models.CharField(max_length=40,verbose_name='Version del Caso de Prueba')
  ambiente = models.CharField(max_length=40,verbose_name='Ambiente de Prueba')
  autorcaso = models.ForeignKey(User)
  probador = models.ForeignKey(User, related_name='relacion_probador_casoprueba', blank=True, null=True)
  fecha = models.DateField('Fecha de Creacion')
  fechaejec = models.DateField('Fecha de Ejecucion',null=True,blank=True)
  condicion = models.TextField(max_length=400,verbose_name='Condicion(es) para que se ejecute el Caso de Prueba')
  criterios = models.TextField(max_length=400,verbose_name='Criterios de Aprobacion del Caso de Prueba')
  desicion = models.CharField(max_length=40,verbose_name='Desicion de Aprobacion del Caso de Prueba')
  fechaapro = models.DateField('Fecha de Aprobacion',null=True,blank=True)

class EjecucionCasoPrueba(models.Model):
  caso = models.ForeignKey(CasoPruebaDetalle)
  paso = models.CharField(max_length=40)
  condicion = models.CharField(max_length=40)
  valor = models.CharField(max_length=40)
  resultadoesp = models.CharField(max_length=40,verbose_name='Resultado Esperado')
  resultadoobt = models.CharField(max_length=40,verbose_name='Resultado Obtenido')
