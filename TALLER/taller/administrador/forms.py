#encoding:utf-8
from django.forms import ModelForm
from django import forms
from administrador.models import UserProfile

class ProfileForm(forms.Form):
  class Meta:
    model = UserProfile
