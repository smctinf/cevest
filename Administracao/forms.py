from django import forms
from django.forms import ModelForm
from cevest.models import Turma

class EscolherTurma(forms.Form):
    turma = forms.ModelChoiceField(queryset=Turma.objects.all())

class login(forms.Form):
    username = forms.CharField(label='Usuário:',max_length=50)
    password = forms.CharField(label='Senha:',max_length=50,widget=forms.PasswordInput())

#class Altera_Situacao(forms.Form):
#    situacao = forms.ChoiceField(widget=forms.RadioSelect,queryset=Situacao.objects.all())
