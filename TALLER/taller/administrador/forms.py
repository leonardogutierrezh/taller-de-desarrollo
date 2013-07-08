#encoding:utf-8
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from administrador.models import Perfil, Proyecto, Miembro, Requerimiento, Iteracion, Sistema, Caracteristica, CasosDeUso, Escenario, EscenarioExtra, EscenarioValor, CasoPrueba, CasoPruebaExtra, CasoPruebaValor

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

class EscenarioForm(forms.ModelForm):
  class Meta:
    model=Escenario
    exclude=['caso','numero']

class EscenarioExtraForm(forms.ModelForm):
  class Meta:
    model=EscenarioExtra
    exclude=['sistema']

class EscenarioValorForm(forms.ModelForm):
  class Meta:
    model=EscenarioValor
    exclude=['escenario','titulo']

class EscenarioDefineForm(forms.Form):
  numeroEscenarios = forms.IntegerField(label='Numero de escenarios')
  numeroCampos = forms.IntegerField(label='Numero de campos adicionales')

class CasoPruebaForm(forms.ModelForm):
  class Meta:
    model=CasoPrueba
    exclude=['escenario']

class CasoPruebaExtraForm(forms.ModelForm):
  class Meta:
    model=CasoPruebaExtra
    exclude=['sistema']

class CasoPruebaValorForm(forms.ModelForm):
  class Meta:
    model=CasoPruebaValor
    exclude=['caso','titulo']

class CasoPruebaDefineForm(forms.Form):
  numeroCasos = forms.IntegerField(label='Numero de casos de prueba')
  numeroCampos = forms.IntegerField(label='Numero de campos adicionales')
