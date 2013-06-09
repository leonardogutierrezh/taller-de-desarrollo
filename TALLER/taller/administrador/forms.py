#encoding:utf-8
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from administrador.models import Perfil, Proyecto, Miembro, Requerimiento, Iteracion, Sistema, Caracteristica, CasosDeUso

class UserForm(forms.ModelForm):
  class Meta:
    model = Perfil
    exclude = ['usuario']

class ProyectoForm(forms.ModelForm):
  class Meta:
    model = Proyecto
    exclude = ['iteActual']

class MiembroForm(forms.ModelForm):
  class Meta:
    model = Miembro
    exclude = ['proyecto']

class SistemaForm(forms.ModelForm):
  class Meta:
    model = Sistema

class ProyectoeForm(forms.ModelForm):
  class Meta:
    model = Proyecto
    exclude = ['nombre']

class RequerimientoForm(forms.ModelForm):
  class Meta:
    model = Requerimiento
    exclude = ['sistema']

class IteracionForm(forms.ModelForm):
  class Meta:
    model = Iteracion
    exclude = ['proyecto','status','numero']

class CaracteristicaForm(forms.ModelForm):
  class Meta:
    model = Caracteristica
    exclude= ['sistema']

class CasosDeUsoForm(forms.ModelForm):
  class Meta:
    model = CasosDeUso
    exclude= ['sistema']
