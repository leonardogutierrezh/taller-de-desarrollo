#encoding:utf-8
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from administrador.models import Perfil, Proyecto, Miembro

class UserForm(forms.ModelForm):
  class Meta:
    model = Perfil
    exclude = ['usuario']

class ProyectoForm(forms.ModelForm):
  class Meta:
    model = Proyecto

class MiembroForm(forms.ModelForm):
  class Meta:
    model = Miembro
    exclude = ['proyecto']
