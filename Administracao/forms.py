from django import forms
from django.forms import ModelForm
from cevest.models import Turma, Situacao

class EscolherTurma(forms.Form):
    turma = forms.ModelChoiceField(queryset=Turma.objects.all())

class login(forms.Form):
    username = forms.CharField(label='Usuário:',max_length=50)
    password = forms.CharField(label='Senha:',max_length=50,widget=forms.PasswordInput())

class Altera_Situacao(forms.Form):
    nome = forms.CharField(label='Aluno:',disabled = True, max_length=100, required=False)
    situacao = forms.ModelChoiceField(widget=forms.Select,queryset=Situacao.objects.all())
