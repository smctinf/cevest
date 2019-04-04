from django import forms
from .models import Aluno, Curso, Bairro, Escolaridade, Profissao, Escolaridade, Turma_Prevista, Turno, Cidade
from django.forms import ModelForm

class Recibo_IndForm(forms.Form):
    codigo = forms.CharField(label='Código:', max_length=5)

YEARS= [x for x in range(1940,2021)]

class CadastroForm(forms.ModelForm):
    dt_nascimento = forms.DateField(label='Dt.Nascimento:', initial="1990-06-21", widget=forms.SelectDateWidget(years=YEARS))
#    cidade = forms.CharField(label='Cidade:', max_length=11)
    class Meta:
        model = Aluno
        exclude = ['ativo','ordem_judicial']
        widgets = {'disponibilidade': forms.CheckboxSelectMultiple, 'cursos': forms.CheckboxSelectMultiple}
#        widgets = {'curso': forms.CheckboxSelectMultiple}
#   curso = forms.ModelMultipleChoiceField(queryset=Curso.objects.all(), widget=forms.CheckboxSelectMultiple)

class AlteraForm(forms.Form):
    cpf = forms.CharField(label='CPF:', max_length=11)
    dt_nascimento = forms.DateField(label='Dt.Nascimento:', initial="1990-06-21", widget=forms.SelectDateWidget(years=YEARS))

class DetalheForm(forms.Form):
    cpf = forms.CharField(label='CPF:', max_length=11)
    dt_nascimento = forms.DateField(label='Dt.Nascimento:', initial="1990-06-21", widget=forms.SelectDateWidget(years=YEARS))

class ConfirmaTurmaForm(forms.Form):
#    cpf = forms.CharField(label='CPF:', max_length=11)
    turma = forms.ModelChoiceField(queryset=Turma_Prevista.objects.all())

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

class CadForm(forms.ModelForm):

        SEX_CHOICES = (
                ('F', 'Feminino',),
                ('M', 'Masculino',),
        )
        
        nome = forms.CharField(max_length=60)
        #cpf = forms.CharField(label='CPF:', max_length=11)
        email = forms.EmailField(label='E-Mail:',max_length=254)
        nis = forms.IntegerField()
        sexo = forms.ChoiceField(widget=forms.RadioSelect, choices=SEX_CHOICES)
        quant_filhos = forms.IntegerField()
        dt_nascimento = forms.DateField(label='Dt.Nascimento:', initial="1990-06-21", widget=forms.SelectDateWidget(years=YEARS))
        bolsa_familia = forms.BooleanField(required=False)
        portador_necessidades_especiais = forms.BooleanField(required=False)
        disponibilidade = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Turno.objects.all())

        celular = forms.CharField(max_length=11)
        fixo_residencia = forms.CharField(max_length=10)
        fixo_trabalho = forms.CharField(max_length=10)
        cidade = forms.ModelChoiceField(queryset=Cidade.objects.all())
        bairro = forms.ModelChoiceField(queryset=Bairro.objects.all())
        cep = forms.CharField(label = 'CEP:')
        endereco = forms.CharField(label='Endereço:',max_length=120)
        escolaridade = forms.ModelChoiceField(queryset=Escolaridade.objects.all())
        profissao = forms.ModelChoiceField(queryset=Profissao.objects.all())
        desempregado = forms.BooleanField(required=False)
        
        class Meta:
            model = Aluno
            fields = ['nome','cpf','email','nis','sexo','quant_filhos','dt_nascimento', 'bolsa_familia',
            'portador_necessidades_especiais', 'disponibilidade', 'celular','fixo_residencia','fixo_trabalho',
            'cidade','bairro','cep','endereco','escolaridade','profissao','desempregado']
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['nis'].required = False
"""
        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self.fields['bairro'].queryset = Bairro.objects.none()
            if 'cidade' in self.data:
                try:
                    cidade_temp = int(self.data.get('cidade'))
                    self.fields['bairro'].queryset = Bairro.objects.queryset.filter(cidade=cidade_temp)
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
"""
"""
#        disponibilidade = forms.CharField(max_length=1, choices=TURNO)
#        curso = forms.ModelMultipleChoiceField(queryset=Curso.objects.all(), widget=forms.CheckboxSelectMultiple)

#        dt_nascimento = forms.DateField(label='Dt.Nascimento:', initial="1990-06-21", widget=forms.SelectDateWidget(years=YEARS))
 #       curso = forms.ModelMultipleChoiceField (widget = forms.CheckboxSelectMultiple())
#        class Meta:
#            model = Aluno
#           fields = '__all__'
#            exclude = ['ativo']
#            widgets = {'disponibilidade': forms.CheckboxSelectMultiple}
#            filter_horizontal = {'cursos'}
"""
"""
    dt_inclusao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
"""

class Altera_cpf(forms.Form):
        cpf = forms.CharField(label='CPF:', max_length=11)
        def getCPF(self):
            return self.cpf
        #dt_nascimento = forms.CharField(widget=forms.DateField)

class Altera_Cadastro(CadForm):
    class Meta(CadForm.Meta):
        exclude = ('cpf',)
    

