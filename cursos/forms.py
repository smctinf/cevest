
import datetime
from time import strptime
from django import forms
from django.forms import ModelForm, ValidationError
from .models import *


class Aluno_form(ModelForm):

    class Meta:
        model = Aluno
        widgets = {
            'turmas': forms.CheckboxSelectMultiple(),
            'celular': forms.TextInput(attrs={'onkeydown': 'mascara(this, icelular)'}),
            'cep': forms.TextInput(attrs={'onkeydown': 'mascara(this, icep)'}),
            'cpf': forms.TextInput(attrs={'onkeydown': 'mascara(this, icpf)'}),
            'rg': forms.TextInput(attrs={'onkeydown': 'mascara(this, irg)'}),
            'dt_nascimento': forms.TextInput(attrs={'type': 'date'}),
            'aceita_mais_informacoes': forms.CheckboxInput(attrs={'required': True}),
            'li_e_aceito_termos': forms.CheckboxInput(attrs={'required': True}),

            'dt_nascimento': forms.widgets.DateInput(attrs={'type': 'date'}),
            'user_inclusao': forms.HiddenInput(),
            'user_ultima_alteracao': forms.HiddenInput(),
        }
            
        exclude = ['dt_inclusao', 'dt_alteracao', 'pessoa']


class CadastroProfessorForm(ModelForm):

    class Meta:
        model = Instrutor
        widgets = {
            'cpf': forms.TextInput(attrs={'onkeydown': 'mascara(this, icpf)'}),
            'celular': forms.TextInput(attrs={'onkeydown': 'mascara(this, icelular)'}),
        }
        exclude = ['dt_inclusao']


class CadastroCursoForm(ModelForm):

    class Meta:
        model = Curso
        widgets = {
            'dt_nascimento': forms.widgets.DateInput(attrs={'type': 'date'}),
        }
        exclude = ['dt_inclusao', 'dt_alteracao', 'user_inclusao']

    def clean_sigla(self):
        sigla = self.cleaned_data['sigla']


        if not sigla.isalpha():
            raise ValidationError("A sigla deve conter apenas letras")
        
        return sigla.capitalize()


class CadastroTurmaForm(ModelForm):

    class Meta:
        model = Turma
        widgets = {
            'data_inicio': forms.TextInput(attrs={'type': 'date'}),
            'data_final': forms.TextInput(attrs={'type': 'date'}),
            'instrutor': forms.CheckboxSelectMultiple()
        }
        exclude = ['dt_inclusao', 'dt_alteracao', 'turnos', 'nome', 'user_ultima_alteracao', 'user_inclusao']


class CadastroCategoriaForm(ModelForm):

    class Meta:
        model = Categoria
        exclude = []


class CadastroLocalForm(ModelForm):

    class Meta:
        model = Local
        widgets = {
            'ativo': forms.HiddenInput(),
            'cep': forms.TextInput(attrs={'onkeydown': 'mascara(this, icep)'}),
        }
        exclude = []


class CadastroAlunoForm(ModelForm):

    class Meta:
        model = Aluno
        widgets = {
            'celular': forms.TextInput(attrs={'onkeydown': 'mascara(this, icelular)'}),
            'dt_nascimento': forms.TextInput(attrs={'type': 'date'}),
            'cpf': forms.TextInput(attrs={'onkeydown': 'mascara(this, icpf)'}),

        }
        exclude = []


class CadastroResponsavelForm(ModelForm):

    class Meta:
        model = Responsavel
        widgets = {
            'celular': forms.TextInput(attrs={'onkeydown': 'mascara(this, icelular)'}),
            'dt_nascimento': forms.TextInput(attrs={'type': 'date'}),
            'cep': forms.TextInput(attrs={'onkeydown': 'mascara(this, icep)'}),
            'rg': forms.TextInput(attrs={'onkeydown': 'mascara(this, irg)'}),
            'cpf': forms.TextInput(attrs={'onkeydown': 'mascara(this, icpf)'}),

        }
        exclude = ['aluno']

class Instituicao_form(ModelForm):

    class Meta:
        model = Instituicao
        exclude = []

    def clean_sigla(self):
        sigla = self.cleaned_data['sigla']


        if not sigla.isalpha():
            raise ValidationError("A sigla deve conter apenas letras")
        
        return sigla.capitalize()

class Turno_form(ModelForm):

    class Meta:
        model=Turno
        exclude = []


class ChoiceField_no_validation(forms.ChoiceField):
    def validate(self, value):
        """Validate that the input is in self.choices."""
        
    def valid_value(self, value):
        """Check to see if the provided value is a valid choice."""
        return True
    
    def to_python(self, value):
        return Turno_estabelecido.objects.get(pk=value)
        
class Aula_form(ModelForm):

    class Meta:
        model=Aula
        exclude = []
    
    associacao_turma_turno = ChoiceField_no_validation(label='Turno', choices=[])
    dt_aula = forms.DateField(label='Data da aula',widget=forms.DateInput(attrs={'type': 'date'}))


    def clean_dt_aula(self):
        dt_aula = self.cleaned_data['dt_aula']
        associacao_turma_turno = self.cleaned_data['associacao_turma_turno']

        if int(associacao_turma_turno.turno.dia_semana) != (dt_aula.weekday() + 1) % 7 + 1:
            raise ValidationError("Dia da semana da aula não corresponde com o turno")

        return dt_aula 
    

class Justificativa_form(ModelForm):

    class Meta:
        model=Justificativa
        exclude = []

    descricao = forms.CharField(widget=forms.Textarea)
