from django import forms
from django.forms import ModelForm, ValidationError
from .models import *

class Tipo_Material_Form(ModelForm):    
    
    class Meta:
        model = Tipo_Material
        # widgets = {
        #     'turmas': forms.CheckboxSelectMultiple(),
        #     'celular': forms.TextInput(attrs={'onkeydown':'mascara(this, icelular)'}),
        #     'cep': forms.TextInput(attrs={'onkeydown':'mascara(this, icep)'}),
        #     'cpf': forms.TextInput(attrs={'onkeydown':'mascara(this, icpf)'}),
        #     'rg': forms.TextInput(attrs={'onkeydown':'mascara(this, irg)'}),
        #     'dt_nascimento': forms.TextInput(attrs={'type':'date'}),
        #     'aceita_mais_informacoes': forms.CheckboxInput(attrs={'required':True}),
        #     'user_inclusao': forms.HiddenInput(),
        #     'user_ultima_alteracao': forms.HiddenInput(),
        # }
        exclude = ['dt_inclusao']

class Material_Form(ModelForm):    
    
    class Meta:
        model = Material        
        exclude = ['dt_inclusao', 'qnt_em_estoque']

class Exibir_Tipo_Material_Form(ModelForm):    
    
    class Meta:
        model = Material        
        exclude = ['dt_inclusao', 'nome', 'qnt_em_estoque']

class Log_estoque_Form(ModelForm):    
    
    class Meta:
        model = Log_estoque
        widgets={'tipo_movimentacao': forms.HiddenInput()}
        exclude = ['dt_inclusao', 'qnt_em_estoque']
