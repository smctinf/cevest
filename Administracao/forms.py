from django import forms
from django.forms import ModelForm
from cevest.models import Turma, Situacao
from django.utils.safestring import mark_safe

class EscolherTurma(forms.Form):
    turma = forms.ModelChoiceField(queryset=Turma.objects.all())

class login(forms.Form):
    username = forms.CharField(label='Usuário:',max_length=50)
    password = forms.CharField(label='Senha:',max_length=50,widget=forms.PasswordInput())

class Altera_Situacao(forms.Form):
    nome = forms.CharField(label='Aluno:',disabled = True, max_length=100, required=False)
    situacao = forms.ModelChoiceField(widget=forms.Select,queryset=Situacao.objects.all())

class HorizontalCheckbox(forms.CheckboxSelectMultiple):
    def render(self,*args,**kwargs):
        output = super(HorizontalCheckbox,self).render(*args,**kwargs)
        return mark_safe(output.replace(u'<li>',u''))

class Controle_Presenca(forms.Form):
    nome = forms.CharField(label='Aluno:',disabled = True, max_length=100, required=False)
    dias = forms.MultipleChoiceField(widget=HorizontalCheckbox, required = False)
    #dia = forms.ChoiceField(widget=forms.CheckboxInput, label = '')
    def __init__(self, *args, CHOICES,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['dias'].choices = CHOICES
