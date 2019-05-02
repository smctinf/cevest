from django import forms
from .models import Aluno, Curso, Bairro, Escolaridade, Profissao, Escolaridade,Turma, Turma_Prevista, Turno, Cidade, Situacao
from django.forms import ModelForm
from .functions import validate_CPF

class Recibo_IndForm(forms.Form):
    codigo = forms.CharField(label='Código:', max_length=5)

YEARS= [x for x in range(1940,2021)]

class DetalheForm(forms.Form):
    cpf = forms.CharField(label='CPF:', max_length=11)
    dt_nascimento = forms.DateField(label='Dt.Nascimento:', initial="1990-06-21", widget=forms.SelectDateWidget(years=YEARS))

class ConfirmaTurmaForm(forms.Form):
#    cpf = forms.CharField(label='CPF:', max_length=11)
    turma = forms.ModelChoiceField(queryset=Turma_Prevista.objects.all())


class CadForm(forms.ModelForm):

        SEX_CHOICES = (
                ('F', 'Feminino',),
                ('M', 'Masculino',),
        )
        cursos = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class' : "custom-control-input"}),queryset=Curso.objects.all())
        nome = forms.CharField(label = "Nome", max_length=60, widget = forms.TextInput(attrs={'class': 'form-control'}) )
        cpf = forms.CharField(label='CPF', max_length=14, widget = forms.TextInput(attrs={'class': 'form-control','onkeydown':"mascara(this,icpf)"}))
        email = forms.EmailField(label='E-Mail',max_length=254,  widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'fulano@exemplo.com.br'}))
        nis = forms.IntegerField(label='NIS', widget = forms.TextInput(attrs={'class': 'form-control'}))
        sexo = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class' : "custom-control-input"}), choices=SEX_CHOICES)
        quant_filhos = forms.IntegerField(label='Quantidade de filhos', widget = forms.TextInput(attrs={'class': 'form-control'}))
        dt_nascimento = forms.DateField(label='Data de Nascimento:', widget = forms.TextInput(attrs={'class': 'form-control',"placeholder":"21/06/1990"}))
        bolsa_familia = forms.BooleanField(label = 'Cadastrado no Bolsa Família.',required=False, widget=forms.CheckboxInput(attrs={'class' : "custom-control-input"}))
        portador_necessidades_especiais = forms.BooleanField(label = 'Portador de Necessidades Especiais.',required=False,widget=forms.CheckboxInput(attrs={'class' : "custom-control-input"}))
        disponibilidade = forms.ModelMultipleChoiceField(label = 'Disponibilidade', widget=forms.CheckboxSelectMultiple(attrs={'class' : "custom-control-input"}),queryset=Turno.objects.all())

        celular = forms.CharField(label= "Celular", max_length=15, widget = forms.TextInput(attrs={'class': 'form-control','onkeydown':"mascara(this,icelular)"}))
        fixo_residencia = forms.CharField(label = "Tel. Residência", max_length=14, widget = forms.TextInput(attrs={'class': 'form-control','onkeydown':"mascara(this,telefone)"}))
        fixo_trabalho = forms.CharField(label = "Tel. Trabalho",max_length=14, widget = forms.TextInput(attrs={'class': 'form-control','onkeydown':"mascara(this,telefone)"}))
        cidade = forms.ModelChoiceField(queryset=Cidade.objects.all(), widget = forms.Select(attrs={'class': "custom-select d-block w-100 cidades"}))
        bairro = forms.ModelChoiceField(queryset=Bairro.objects.all(), widget = forms.Select(attrs={'class': 'form-control'}))
        cep = forms.CharField(label = 'CEP', max_length= 9, widget = forms.TextInput(attrs={'class': 'form-control'}))
        endereco = forms.CharField(label='Endereço',max_length=120, widget = forms.TextInput(attrs={'class': 'form-control'}))
        complemento = forms.CharField(label='Complemento',max_length=120, widget = forms.TextInput(attrs={'class': 'form-control'}))

        escolaridade = forms.ModelChoiceField(label = 'Escolaridade',queryset=Escolaridade.objects.all(), widget = forms.Select(attrs={'class': "custom-select d-block w-100 cidades"}))

        profissao = forms.ModelChoiceField(label = 'Profissão',queryset=Profissao.objects.all(), widget = forms.Select(attrs={'class': "custom-select d-block w-100 cidades"}))
        desempregado = forms.BooleanField(label = 'Desempregado',required=False,widget=forms.CheckboxInput(attrs={'class' : "custom-control-input"}))
        outra_profissao = forms.CharField(label='Outra Profissão',max_length=60, widget = forms.TextInput(attrs={'class': 'form-control'}))

        class Meta:
            model = Aluno
            fields = ['cursos', 'nome','cpf','email','nis','sexo','quant_filhos','dt_nascimento', 'bolsa_familia',
            'portador_necessidades_especiais', 'disponibilidade', 'celular','fixo_residencia','fixo_trabalho',
            'cidade','bairro','cep','endereco','complemento','profissao','escolaridade','desempregado','outra_profissao']
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['nis'].required = False

        def clean_nome(self):
            nome = self.cleaned_data["nome"]
            nome = nome.lower()
            nome = nome.title()
            return nome

        def clean_cpf(self):
            cpf = self.cleaned_data["cpf"]
            cpf = cpf.replace('.','')
            cpf = cpf.replace('-','')
            return cpf

        def clean_celular(self):
            telefone = self.cleaned_data["celular"]
            telefone = telefone.replace("(",'')
            telefone = telefone.replace(")",'')
            telefone = telefone.replace("-",'')
            telefone = telefone.replace(" ",'')
            return telefone
        
        def clean_fixo_residencia(self):
            telefone = self.cleaned_data["fixo_residencia"]
            telefone = telefone.replace("(",'')
            telefone = telefone.replace(")",'')
            telefone = telefone.replace("-",'')
            telefone = telefone.replace(" ",'')        
            return telefone

        def clean_fixo_trabalho(self):
            telefone = self.cleaned_data["fixo_trabalho"]
            telefone = telefone.replace("(",'')
            telefone = telefone.replace(")",'')
            telefone = telefone.replace("-",'')
            telefone = telefone.replace(" ",'')
            return telefone

        def clean_cep(self):
            cep = self.cleaned_data["cep"]
            cep = cep.replace("-",'')
            return cep

            
class Altera_cpf(forms.Form):
        cpf = forms.CharField(label='CPF:', max_length=11)
        dt_nascimento = forms.DateField(label='Data de nascimento:', initial="1990-06-21", widget=forms.SelectDateWidget(years=YEARS))

        def clean_cpf(self):
            cpf = validate_CPF(self.cleaned_data["cpf"])
            return cpf
        #dt_nascimento = forms.CharField(widget=forms.DateField)

class Altera_Cadastro(CadForm):
    class Meta(CadForm.Meta):
        exclude = ('cpf',)