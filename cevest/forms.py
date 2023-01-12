from django import forms
from .models import *
from django.forms import ValidationError
from .functions import validate_CPF
import datetime


class Recibo_IndForm(forms.Form):
    codigo = forms.CharField(label='Código:', max_length=5)


class DetalheForm(forms.Form):
    cpf = forms.CharField(label='CPF:', max_length=11)
    dt_nascimento = forms.DateField(label='Dt.Nascimento:', initial="1990-06-21",
                                    widget=forms.SelectDateWidget(years=[x for x in range(1940, datetime.datetime.now().year)]))


class ConfirmaTurmaForm(forms.Form):
    turma = forms.ModelChoiceField(queryset=Turma_Prevista.objects.all())


class CadFormBase(forms.ModelForm):

    SEXO_CHOICES = (
        ('F', 'Feminino',),
        ('M', 'Masculino',),
    )

    cursos = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(
        attrs={'class': "custom-control-input"}), queryset=Curso.objects.filter(exibir=True).filter(ativo=True).order_by('-programa').order_by('nome'))
    nome = forms.CharField(label="Nome", max_length=60, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-Mail', max_length=254,  widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'fulano@exemplo.com.br'}))
    nis = forms.IntegerField(label='NIS', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'maxlength': '11'}))
    sexo = forms.ChoiceField(widget=forms.RadioSelect(
        attrs={'class': "custom-control-input"}), choices=SEXO_CHOICES)
    quant_filhos = forms.IntegerField(
        label='Quantidade de filhos', initial=0, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dt_nascimento = forms.DateField(label='Data de Nascimento:', widget=forms.DateInput(
        attrs={'class': 'form-control', 'placeholder': 'DD/MM/AAAA', 'oninput': 'mascara(this,data)', 'onload': 'mascara(this,data)', 'maxlength': '10'}))
    bolsa_familia = forms.BooleanField(label='Cadastrado no Bolsa Família.', required=False,
                                       widget=forms.CheckboxInput(attrs={'class': "custom-control-input"}))
    portador_necessidades_especiais = forms.BooleanField(
        label='Portador de Necessidades Especiais.', required=False, widget=forms.CheckboxInput(attrs={'class': "custom-control-input"}))
    disponibilidade = forms.ModelMultipleChoiceField(label='Disponibilidade', widget=forms.CheckboxSelectMultiple(
        attrs={'class': "custom-control-input"}), queryset=Turno.objects.all())

    celular = forms.CharField(label="Celular", max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control', 'oninput': "mascara(this,icelular)", 'onload': 'mascara(this,icelular)'}))
    fixo_residencia = forms.CharField(label="Tel. Residência", required=False, max_length=14, widget=forms.TextInput(
        attrs={'class': 'form-control', 'oninput': "mascara(this,telefone)", 'onload': 'mascara(this,telefone)'}))
    fixo_trabalho = forms.CharField(label="Tel. Trabalho", required=False, max_length=14, widget=forms.TextInput(
        attrs={'class': 'form-control', 'oninput': "mascara(this,telefone)", 'onload': 'mascara(this,telefone)'}))
    cidade = forms.ModelChoiceField(queryset=Cidade.objects.all(), widget=forms.Select(
        attrs={'class': "custom-select d-block w-100 cidades teste"}))
    bairro = forms.ModelChoiceField(queryset=Bairro.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control'}))
    cep = forms.CharField(label='CEP', max_length=9, widget=forms.TextInput(attrs={
                          'class': 'form-control', 'oninput': "getCEP(this.value)", 'onkeyup': 'mascara(this,icep)', 'onload': 'mascara(this,icep)'}))
    endereco = forms.CharField(label='Endereço', max_length=120, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    complemento = forms.CharField(label='Complemento', required=False,
                                  max_length=120, widget=forms.TextInput(attrs={'class': 'form-control'}))

    escolaridade = forms.ModelChoiceField(label='Escolaridade', queryset=Escolaridade.objects.all(
    ), widget=forms.Select(attrs={'class': "custom-select d-block w-100 cidades"}))

    profissao = forms.ModelChoiceField(label='Profissão', queryset=Profissao.objects.all(
    ), widget=forms.Select(attrs={'class': "custom-select d-block w-100 cidades"}))
    desempregado = forms.BooleanField(label='Desempregado', required=False, widget=forms.CheckboxInput(
        attrs={'class': "custom-control-input"}))
    outra_profissao = forms.CharField(label='Outra Profissão', max_length=60, widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Aluno
        fields = ['cursos', 'nome', 'email', 'nis', 'sexo', 'quant_filhos', 'dt_nascimento', 'bolsa_familia',
                  'portador_necessidades_especiais', 'disponibilidade', 'celular', 'fixo_residencia', 'fixo_trabalho',
                  'cidade', 'bairro', 'cep', 'endereco', 'complemento', 'profissao', 'escolaridade', 'desempregado', 'outra_profissao']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nis'].required = False
        self.fields['email'].required = False
        self.fields['bairro'].queryset = Bairro.objects.none()
        if 'cidade' in self.data:
            try:
                cidade_id = int(self.data.get('cidade'))
                self.fields['bairro'].queryset = Bairro.objects.filter(
                    cidade=cidade_id).order_by('nome')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            temp_bairro = Bairro.objects.get(id=self.instance.bairro.id)
            self.fields['bairro'].queryset = Bairro.objects.filter(
                cidade=temp_bairro.cidade)
            self.fields['bairro'].initial = temp_bairro

    def clean_nome(self):
        nome = self.cleaned_data["nome"].strip()

        print('nome: ', nome, nome.find(' '))

        if nome.find(' ') == -1:
            raise ValidationError('Insira seu nome completo')
        else:
            nome = nome.lower()
            nome = nome.title()
            return nome

    def clean_celular(self):
        telefone = self.cleaned_data["celular"]
        telefone = telefone.replace("(", '')
        telefone = telefone.replace(")", '')
        telefone = telefone.replace("-", '')
        telefone = telefone.replace(" ", '')
        if len(telefone) == 10:
            if telefone[2:3] != '2':
                raise ValidationError('Insira um número válido ')
        else:
            if len(telefone) != 11:
                raise ValidationError('Insira um número válido ')
        return telefone

    def clean_fixo_residencia(self):
        telefone = self.cleaned_data["fixo_residencia"]
        telefone = telefone.replace("(", '')
        telefone = telefone.replace(")", '')
        telefone = telefone.replace("-", '')
        telefone = telefone.replace(" ", '')
        if len(telefone) != 10 and len(telefone) != 0:
            raise ValidationError('Insira um número válido')
        return telefone

    def clean_fixo_trabalho(self):
        telefone = self.cleaned_data["fixo_trabalho"]
        telefone = telefone.replace("(", '')
        telefone = telefone.replace(")", '')
        telefone = telefone.replace("-", '')
        telefone = telefone.replace(" ", '')
        if len(telefone) != 10 and len(telefone) != 0:
            raise ValidationError('Insira um número válido')
        return telefone

    def clean_cep(self):
        cep = self.cleaned_data["cep"]
        cep = cep.replace("-", '')
        if len(cep) != 8:
            raise ValidationError('Insira um CEP válido')
        return cep

    def clean_nis(self):
        nis = self.cleaned_data["nis"]

        if nis == None:
            return

        nis = str(nis)

        if len(nis) != 11 and len(nis) != 0:
            raise ValidationError('Insira um NIS válido')
        else:
            return nis

    def clean_dt_nascimento(self):
        dt_nasc = self.cleaned_data["dt_nascimento"]

        deltatime = dt_nasc - datetime.date.today()
        if datetime.timedelta(days=-14*365) < deltatime or deltatime < datetime.timedelta(days=-120*365):
            raise ValidationError('Insira uma data válida')
        else:
            return dt_nasc


class CadForm(CadFormBase):
    cpf = forms.CharField(label='CPF', max_length=14, widget=forms.TextInput(
        attrs={'class': 'form-control', 'oninput': "mascara(this,icpf)"}))
    cpf_file = forms.FileField(label='Anexo em PDF do que possua seu CPF', widget=forms.FileInput(
        attrs={'class': 'form-control', 'required': False,'accept': 'application/pdf', 'enctype': "multipart/form-data"}))
    identidade_file = forms.FileField(label='Anexo em PDF do documento de identidade', widget=forms.FileInput(
        attrs={'class': 'form-control', 'accept': 'application/pdf', 'enctype': "multipart/form-data"}))
    comprovante_residencia_file = forms.FileField(label='Anexo em PDF do comprovante de residência', widget=forms.FileInput(
        attrs={'class': 'form-control', 'accept': 'application/pdf', 'enctype': "multipart/form-data"}))

    class Meta(CadFormBase.Meta):
        fields = ['cursos', 'nome', 'cpf', 'email', 'nis', 'sexo', 'quant_filhos', 'dt_nascimento', 'bolsa_familia',
                  'portador_necessidades_especiais', 'disponibilidade', 'celular', 'fixo_residencia', 'fixo_trabalho',
                  'cidade', 'bairro', 'cep', 'endereco', 'complemento', 'profissao', 'escolaridade', 'desempregado', 'outra_profissao', 'cpf_file', 'identidade_file', 'comprovante_residencia_file']

    def clean_cpf(self):
        cpf = validate_CPF(self.cleaned_data["cpf"])
        return cpf

    def __init__(self, *args, **kwargs):
        super(CadForm, self).__init__(*args, **kwargs)
        self.fields['cpf_file'].required = False
        self.fields['identidade_file'].required = False
        self.fields['comprovante_residencia_file'].required = False        

class Altera_cpf(forms.Form):
    cpf = forms.CharField(label='CPF:', max_length=14, widget=forms.TextInput(
        attrs={'class': 'form-control', 'oninput': "mascara(this,icpf)"}))
    dt_nascimento = forms.DateField(label='Data de Nascimento:', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'DD/MM/AAAA', 'oninput': 'mascara(this,data)', 'maxlength': '10'}))

    def clean_cpf(self):
        cpf = validate_CPF(self.cleaned_data["cpf"])
        return cpf

# class Altera_Cadastro(CadForm):
#     def __init__(self,*args,**kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['cpf'] = None

#     def clean_cpf(self):
#         return


class TesteForm(forms.ModelForm):
    cidade = forms.ModelChoiceField(
        queryset=Cidade.objects.all(), widget=forms.Select(attrs={'class': 'teste'}))
    #bairro = forms.ModelChoiceField(queryset=Bairro.objects.none())

    class Meta:
        model = Aluno
        fields = ['cidade', 'bairro']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bairro'].queryset = Bairro.objects.none()

        if 'cidade' in self.data:
            try:
                cidade_id = int(self.data.get('cidade'))
                self.fields['bairro'].queryset = Bairro.objects.filter(
                    cidade=cidade_id).order_by('nome')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['bairro'].queryset = self.instance.cidade.bairro_set.order_by(
                'nome')
