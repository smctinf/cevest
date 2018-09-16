from django import forms
from .models import *
from django.forms import ModelForm

class CadastroForm(ModelForm):

    class Meta:
        model = Aluno
#        fields = ['nome', 'cpf']
        fields = '__all__'
#        exclude = ['campo']