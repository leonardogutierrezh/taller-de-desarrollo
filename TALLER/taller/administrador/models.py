#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

class Proyecto(models.Model):
  nombre = models.CharField(max_length=100, unique=True)
  fechaInicio = models.DateField('Fecha de Inicio')
  fechaFin = models.DateField('Fecha de Finalización')
  descripcion = models.TextField(max_length=200)
  metodologia = models.CharField(max_length=100)
  recursos = models.TextField(max_length=200)
  iteraciones = models.IntegerField()
  iteActual = models.IntegerField(default=0)


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
  rol = models.CharField(max_length=100)

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

  def __unicode__(self):
    return self.nombre

class CasosDeUso(models.Model):
  caso= models.CharField(max_length=50)
  sistema= models.ForeignKey(Sistema)
  requerimiento = models.ForeignKey(Requerimiento)
  actor = models.CharField(max_length=50)
  descripcion = models.TextField(max_length=200)
  precondicion = models.TextField(max_length=200)

  def __unicode__(self):
    return self.caso


class Escenario(models.Model):
  caso = models.ForeignKey(CasosDeUso)
  numero= models.TextField(max_length=10,verbose_name='ID Escenario')
  flujoOriginario= models.TextField(max_length=400,verbose_name='Flujo Originario')
  flujoAlterno= models.TextField(max_length=400,verbose_name='Flujo Alterno')

class EscenarioExtra(models.Model):
  sistema= models.ForeignKey(Sistema)
  titulo= models.CharField(max_length=40,verbose_name='Nombre del campo')

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

class CasoPruebaExtra(models.Model):
  sistema= models.ForeignKey(Sistema)
  titulo= models.CharField(max_length=40,verbose_name='Nombre del campo')

class CasoPruebaValor(models.Model):
  caso = models.ForeignKey(CasoPrueba)
  titulo = models.ForeignKey(CasoPruebaExtra)
  valor = models.TextField(max_length=400)
	
