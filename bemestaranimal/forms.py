import unicodedata
from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import *
from autenticacao.functions import validate_cpf

class Form_Tutor(ModelForm):
    class Meta:
        model = Tutor
        widgets = {
            'pessoa':forms.HiddenInput(),
        }
        fields = ['tipo_de_moradia', 'pessoa']

class Form_Tipo(ModelForm):
    class Meta:
        model = Tipo
        fields = ['nome']


class Form_Especie(ModelForm):
    class Meta:
        model = Especie
        fields = ['nome_especie']
        
    def clean_nome_especie(self):
        name = self.cleaned_data.get('nome_especie')
        if name:
            name = name.lower()
            name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode()
        return name


class Form_Animal(ModelForm):    

    class Meta:
        model = Animal
        
        exclude = ['dt_inclusao', 'especie']
        widgets = {
                'tutor': forms.HiddenInput(), 
                'tipo': forms.RadioSelect()}
        
class Form_Catalogo(ModelForm):
    class Meta:
        model= Catalogo
        fields = ['animal', 'pelagem', 'vacinado']
        widgets = {
            'animal':forms.HiddenInput(),
            'castrado': forms.CheckboxInput(attrs={'role':'switch', 'id':'flexSwitchCheckDefault'}),
            'vacinado': forms.CheckboxInput()
        }

class Form_Errante(ModelForm):

    class Meta:
        model = Errante
        exclude = ['dt_inclusao', 'especie']
        widgets = {
            'tipo':forms.RadioSelect(),
        }

class Form_Info_Extras(ModelForm):
    class Meta:
        model = Informacoes_Extras
        fields = ['alimentacao_tipo', 'alimentacao_periodo', 'condicoes', 'dt_vacinacao', 'dt_vermifugacao', 'complemento', 'dt_registro', 'animal']
        widgets = {
            'alimentacao_periodo':forms.CheckboxSelectMultiple(),
            'dt_vacinacao':forms.TextInput(attrs={'type':'date'}),
            'dt_vermifugacao':forms.TextInput(attrs={'type':'date'}),
            'dt_registro':forms.TextInput(attrs={'type':'date'}),
            'animal':forms.HiddenInput()
        }


class Form_EntrevistaPrevia(ModelForm):
    class Meta:
        model = EntrevistaPrevia
        exclude = []
        widgets = {
            'animal':forms.HiddenInput(),
            'cpf':forms.TextInput(attrs={'onkeydown':'mascara(this,icpf)'}),
            'telefone':forms.TextInput(attrs={'onkeydown':'mascara(this, itel)'}),
            'quest_dois':forms.RadioSelect(),
            'quest_tres':forms.RadioSelect(),
            'quest_quatro':forms.RadioSelect(),
            'quest_cinco':forms.RadioSelect(),
            'quest_seis':forms.RadioSelect(),
            'quest_sete':forms.RadioSelect(),
            'quest_oito':forms.RadioSelect(),
            'quest_nove':forms.RadioSelect(),
            'quest_dez':forms.RadioSelect(),
        }
    def clean_cpf(self):
        cpf = validate_cpf(self.cleaned_data["cpf"])
        return cpf

    def clean_telefone(self):
        telefone = self.cleaned_data["telefone"]
        telefone = telefone.replace('(', '')
        telefone = telefone.replace(' ', '')
        telefone = telefone.replace(')', '')
        telefone = telefone.replace('-', '')
        return telefone