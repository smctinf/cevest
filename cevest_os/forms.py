from django import forms
from django.forms import ModelForm, ValidationError
from .models import CEVEST_OrdemDeServico, Funcionario_CEVEST_OS, CEVEST_OS_ext, CEVEST_OS_Linha_Tempo
from autenticacao.models import Pessoa
from django.contrib.auth.models import Group
from django.forms import ModelChoiceField

class OS_Form(ModelForm):    
    
    class Meta:
        model = CEVEST_OrdemDeServico
        widgets = {
            'tipo': forms.Select(attrs={'readonly': True}),
        }
        exclude = ['numero', 'dt_inclusao', 'atendente', 'dt_conclusao', 'prioridade', 'status', 'contribuinte', 'pontos_atendidos', 'cadastrado_por']


class OS_Form_Ponto(ModelForm):    
    
    class Meta:
        model = CEVEST_OrdemDeServico       
        fields = ['pontos_atendidos']

class PessoaChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nome
    
class Funcionario_Form(ModelForm):

    pessoa = PessoaChoiceField(queryset=Pessoa.objects.none(), label='Selecione uma pessoa')

    def __init__(self, *args, **kwargs):
        grupo = kwargs.pop('grupo', None) or Group.objects.get(name='os_funcionario')
        super().__init__(*args, **kwargs)
        if grupo:
            self.fields['pessoa'].queryset = Pessoa.objects.filter(user__groups=grupo)

    class Meta:
        model = Funcionario_CEVEST_OS
        widgets = {'tipo_os': forms.HiddenInput()}
        fields = ['pessoa', 'nivel', 'tipo_os']

class Funcionario_Form_editar(ModelForm):

    pessoa = PessoaChoiceField(queryset=Pessoa.objects.none(), label='Selecione uma pessoa')

    def __init__(self, *args, **kwargs):
        grupo = kwargs.pop('grupo', None) or Group.objects.get(name='os_funcionario')
        super().__init__(*args, **kwargs)
        if grupo:
            self.fields['pessoa'].queryset = Pessoa.objects.filter(user__groups=grupo)

    class Meta:
        model = Funcionario_CEVEST_OS
        widgets = {'tipo_os': forms.HiddenInput()}
        fields = ['pessoa', 'nivel', 'tipo_os']


class Equipe_Form(ModelForm):
    class Meta:
        model = CEVEST_OS_ext
        widgets = {
            'equipe': forms.CheckboxSelectMultiple(),
            'os': forms.HiddenInput()

        }        
        exclude=[]

class NovaMensagemForm(forms.ModelForm):
    class Meta:
        model = CEVEST_OS_Linha_Tempo
        fields = ['os', 'pessoa', 'mensagem', 'anexo']
        widgets = {
            'os': forms.HiddenInput(),
            'pessoa': forms.HiddenInput(),
            'mensagem': forms.Textarea(attrs={'class': 'form-control h-100', 'rows': 6}),
            'anexo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }