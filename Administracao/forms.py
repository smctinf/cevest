from django import forms
from django.forms import ModelForm
from cevest.models import Turma, Situacao,Turma_Prevista, Status_Aluno_Turma_Prevista, Aluno
from django.utils.safestring import mark_safe

class EscolherTurma(forms.Form):
    turma = forms.ModelChoiceField(queryset=Turma.objects.all())

class login(forms.Form):
    username = forms.CharField(label='Usuário:',max_length=50)
    password = forms.CharField(label='Senha:',max_length=50,widget=forms.PasswordInput())

class Altera_Situacao(forms.Form):
    nome = forms.CharField(label='Aluno:',disabled = True, max_length=100, required=False)
    situacao = forms.ModelChoiceField(widget=forms.Select,queryset=Situacao.objects.all())

class Altera_Situacao_Prevista(forms.Form):
    nome = forms.CharField(label='Aluno:',disabled = True, max_length=100, required=False)
    situacao = forms.ModelChoiceField(widget=forms.Select,queryset=Status_Aluno_Turma_Prevista.objects.all())
    aluno_id = forms.IntegerField()

#Tira as tags <li> do widget de checkbox para ele poder ser colocado na horizontal
class HorizontalCheckbox(forms.CheckboxSelectMultiple):
    def render(self,*args,**kwargs):
        output = super(HorizontalCheckbox,self).render(*args,**kwargs)
        return mark_safe(output.replace(u'<li>',u''))

class EscolherDia(forms.Form):
    data = forms.ChoiceField(widget=forms.Select)
    def __init__(self, *args, CHOICES,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['data'].choices = CHOICES

class EscolherTurmaPrevista(forms.Form):
    turma = forms.ModelChoiceField(widget=forms.Select,queryset=None)
    def __init__(self, *args, QUERYSET,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['turma'].queryset = QUERYSET

class Controle_Presenca(forms.Form):
    nome = forms.CharField(label='Aluno:',disabled = True, max_length=100, required=False)
    dias = forms.MultipleChoiceField(widget=HorizontalCheckbox, required = False)
    #dia = forms.ChoiceField(widget=forms.CheckboxInput, label = '')
    def __init__(self, *args, CHOICES,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['dias'].choices = CHOICES

class Confirmar_Turma(forms.Form):
    nome = forms.CharField(label = 'Turma:', disabled = True, required = False)
    confirma = forms.BooleanField(widget=forms.CheckboxInput, required = False)


