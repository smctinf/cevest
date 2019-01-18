from django import forms
from .models import Aluno, Curso, Bairro, Escolaridade, Profissao, Escolaridade
from django.forms import ModelForm

YEARS= [x for x in range(1940,2021)]

class CadastroForm(forms.ModelForm):
    dt_nascimento = forms.DateField(label='Dt.Nascimento:', initial="1990-06-21", widget=forms.SelectDateWidget(years=YEARS))
#    cidade = forms.CharField(label='Cidade:', max_length=11)
    class Meta:
        model = Aluno
        exclude = ['ativo']
        widgets = {'disponibilidade': forms.CheckboxSelectMultiple, 'cursos': forms.CheckboxSelectMultiple}
#        widgets = {'curso': forms.CheckboxSelectMultiple}
#   curso = forms.ModelMultipleChoiceField(queryset=Curso.objects.all(), widget=forms.CheckboxSelectMultiple)

class AlteraForm(forms.Form):
    cpf = forms.CharField(label='CPF:', max_length=11)
    dt_nascimento = forms.DateField(label='Dt.Nascimento:', initial="1990-06-21", widget=forms.SelectDateWidget(years=YEARS))

class DetalheForm(forms.Form):
    cpf = forms.CharField(label='CPF:', max_length=11)
    dt_nascimento = forms.DateField(label='Dt.Nascimento:', initial="1990-06-21", widget=forms.SelectDateWidget(years=YEARS))


"""
class CadastroForm(forms.Form):

   nome = forms.CharField(label='nome', max_length=60)
   curso = forms.ModelMultipleChoiceField(queryset=Curso.objects.all(), widget=forms.CheckboxSelectMultiple)

   class Meta:
        model = Aluno
#        fields = ['nome', 'cpf']
#        fields = '__all__'
#        exclude = ['campo']
"""

class CadForm(forms.Form):

#class CadForm(forms.ModelForm):

        SEX_CHOICES = (
                ('F', 'Feminino',),
                ('M', 'Masculino',),
        )
        nome = forms.CharField(max_length=60)
        email = forms.EmailField(label='E-Mail:',max_length=254)
        cpf = forms.CharField(label='CPF:', max_length=11)
        nis = forms.IntegerField()
        bolsa_familia = forms.BooleanField()
        quant_filhos = forms.IntegerField()
        sexo = forms.ChoiceField(widget=forms.Select, choices=SEX_CHOICES)
        portador_necessidades_especiais = forms.BooleanField()
#        dt_nascimento = forms.CharField(widget=forms.DateField)

        dt_nascimento = forms.DateField(label='Dt.Nascimento:', initial="1990-06-21", widget=forms.SelectDateWidget(years=YEARS))

        celular = forms.CharField(max_length=11)
        fixo_residencia = forms.CharField(max_length=10)
        fixo_trabalho = forms.CharField(max_length=10)
        endereco = forms.CharField(label='Endereço:',max_length=120)
        bairro = forms.ModelChoiceField(queryset=Bairro.objects.all())
        escolaridade = forms.ModelChoiceField(queryset=Escolaridade.objects.all())
        profissao = forms.ModelChoiceField(queryset=Profissao.objects.all())
        desempregado = forms.BooleanField()

"""
#        disponibilidade = forms.CharField(max_length=1, choices=TURNO)
        curso = forms.ModelMultipleChoiceField(queryset=Curso.objects.all(), widget=forms.CheckboxSelectMultiple)

        dt_nascimento = forms.DateField(label='Dt.Nascimento:', initial="1990-06-21", widget=forms.SelectDateWidget(years=YEARS))
 #       curso = forms.ModelMultipleChoiceField (widget = forms.CheckboxSelectMultiple())
        class Meta:
            model = Aluno
#           fields = '__all__'
            exclude = ['ativo']
            widgets = {'disponibilidade': forms.CheckboxSelectMultiple}
#            filter_horizontal = {'cursos'}
"""
"""
    dt_inclusao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
"""

class Altera_cpf(forms.Form):
        cpf = forms.CharField(label='CPF:', max_length=11)
        dt_nascimento = forms.CharField(
#                widget=forms.DateField
        )