from django import forms
from .models import Aluno, Curso
from django.forms import ModelForm

SEXO = ['1','m']


# SEXO = (
#     ('F', 'Feminino'),
#     ('M', 'Masculino'),
# )

class CadastroForm(forms.Form):

   nome = forms.CharField(label='nome', max_length=60)
   curso = forms.ModelMultipleChoiceField(queryset=Curso.objects.all(), widget=forms.CheckboxSelectMultiple)

   class Meta:
        model = Aluno
#        fields = ['nome', 'cpf']
#        fields = '__all__'
#        exclude = ['campo']