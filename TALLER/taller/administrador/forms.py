#encoding:utf-8
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from administrador.models import Perfil

class UserForm(forms.ModelForm):
  class Meta:
    model = Perfil
    exclude = ['usuario']

