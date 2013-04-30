from django.db import models
from django.contrib.auth.models import User

class Proyecto(models.Model):
  nombre = models.CharField(max_length=100)
  fecha = models.DateTimeField('Fecha de Publicacion')
  descripcion = models.TextField(max_length=200)
  metodologia = models.CharField(max_length=100)
       
class Miembro(models.Model):
  usuario = models.ForeignKey(User)
  proyecto = models.ForeignKey(Proyecto)
  rol = models.CharField(max_length=100)

class UserProfile(models.Model):
  telefono = models.CharField(max_length=15)
  direccion = models.CharField(max_length=100)
  cargo = models.CharField(max_length=100)
  #avatar = models.ImageField()
  
	
