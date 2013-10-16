#encoding:utf-8
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from administrador.models import Perfil, Proyecto, Miembro, Requerimiento, Iteracion, Sistema, Caracteristica, CasosDeUso, Escenario, EscenarioExtra, EscenarioValor, CasoPrueba, CasoPruebaExtra, CasoPruebaValor, CasoPruebaDetalle, EjecucionCasoPrueba
from django.forms.extras.widgets import SelectDateWidget

class UserForm(forms.ModelForm):
  class Meta:
    model = Perfil
    exclude = ['usuario']

class ProyectoForm(forms.ModelForm):
  fechaInicio = forms.DateField(widget=SelectDateWidget(), label='fecha de inicio')
  fechaFin = forms.DateField(widget=SelectDateWidget(), label='fecha de finalizacion')
  class Meta:
    model = Proyecto
    exclude = ['iteActual']

class MiembroForm(forms.ModelForm):
  class Meta:
    model = Miembro
    exclude = ['proyecto']

class MiembroForm(forms.Form):
  rol_choices = (
    ('Gerente de Proyecto', 'Gerente de Proyecto'),
    ('Gerente de Pruebas', 'Gerente de Pruebas'),
    ('Analista de Pruebas', 'Analista de Pruebas'),
    ('Disenador de Pruebas', 'Diseñador de Pruebas'),
    ('Cliente', 'Cliente'),
    ('Probador', 'Probador',),
    ('Analista de Requerimiento', 'Analista de Requerimiento'),
    )
  usuario = forms.ModelChoiceField(queryset=User.objects.all())
  rol = forms.MultipleChoiceField(choices=rol_choices, widget=forms.CheckboxSelectMultiple())

class SistemaForm(forms.ModelForm):
  class Meta:
    model = Sistema

class ProyectoeForm(forms.ModelForm):
  fechaInicio = forms.DateField(widget=SelectDateWidget(), label='fecha de inicio')
  fechaFin = forms.DateField(widget=SelectDateWidget(), label='fecha de finalizacion')
  class Meta:
    model = Proyecto
    exclude = ['nombre', 'fechaInicio', 'fechaFin']

class RequerimientoForm(forms.ModelForm):
  class Meta:
    model = Requerimiento
    exclude = ['sistema','nombre','caracteristica','detalle','idrequerimiento']

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
    exclude= ['sistema','actor','caso','detalle']

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
    exclude=['escenario','detalle']

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

class CasoPruebaDetalleForm(forms.ModelForm):
  fecha = forms.DateField(widget=SelectDateWidget(), label='fecha de creacion')
  class Meta:
    model = CasoPruebaDetalle
    exclude = ['casoprueba', 'sistema', 'casouso', 'autorcaso', 'fechaejec', 'fechaapro', 'fecha']
  fecha = forms.DateField(widget=SelectDateWidget(), label='fecha de creacion')
class EjecucionCasoPruebaForm(forms.Form):
  class Meta:
    model=CasoPruebaDetalle
    exclude=['caso'] 

class CasoPruebaDetalleDefineForm(forms.Form):
  numeroCampos = forms.IntegerField(label='Numero de ejecuciones')
