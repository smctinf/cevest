from django import forms
from django.forms import ModelForm, BaseFormSet
from cevest.models import *
from django.utils.safestring import mark_safe


class EscolherTurma(forms.Form):
    def __init__(self, turma_aberta, administrador, INSTRUTOR, *args, **kwargs):
        super(EscolherTurma, self).__init__(*args, **kwargs)
#        turma = forms.ModelChoiceField(queryset=Turma.objects.all())
    #    self.fields['turma'] = forms.ModelChoiceField(queryset=Turma.objects.all())
#        self.fields['turma'].queryset = forms.ModelChoiceField(queryset=Turma.objects.filter(instrutor=INSTRUTOR))

        if turma_aberta == 's':
            if administrador == 's':
                self.fields['turma'] = forms.ModelChoiceField(
                    queryset=Turma.objects.filter(dt_fechamento=None))
            else:
                self.fields['turma'] = forms.ModelChoiceField(
                    queryset=Turma.objects.filter(instrutor=INSTRUTOR).filter(dt_fechamento=None))
        else:
            if administrador == 's':
                self.fields['turma'] = forms.ModelChoiceField(
                    queryset=Turma.objects.exclude(dt_fechamento=None))
            else:
                self.fields['turma'] = forms.ModelChoiceField(
                    queryset=Turma.objects.filter(instrutor=INSTRUTOR).exclude(dt_fechamento=None))


class EscolherTurmaEncerramento(forms.Form):
    def __init__(self, administrador, INSTRUTOR, *args, **kwargs):
        super(EscolherTurmaEncerramento, self).__init__(*args, **kwargs)

        from datetime import date

        hoje = date.today()

        if administrador == 's':
            self.fields['turma'] = forms.ModelChoiceField(
                queryset=Turma.objects.filter(dt_fechamento=None).filter(dt_fim__lte=hoje))
        else:
            self.fields['turma'] = forms.ModelChoiceField(queryset=Turma.objects.filter(
                instrutor=INSTRUTOR).filter(dt_fechamento=None).filter(dt_fim__lte=hoje))


class EscolherTurmaCertificado(forms.Form):
    def __init__(self, administrador, INSTRUTOR, *args, **kwargs):
        super(EscolherTurmaCertificado, self).__init__(*args, **kwargs)
#        turma = forms.ModelChoiceField(queryset=Turma.objects.all())
    #    self.fields['turma'] = forms.ModelChoiceField(queryset=Turma.objects.all())
#        self.fields['turma'].queryset = forms.ModelChoiceField(queryset=Turma.objects.filter(instrutor=INSTRUTOR))

        if administrador == 's':
            self.fields['turma'] = forms.ModelChoiceField(
                queryset=Turma.objects.exclude(dt_fechamento=None))
        else:
            self.fields['turma'] = forms.ModelChoiceField(
                queryset=Turma.objects.filter(instrutor=INSTRUTOR).exclude(dt_fechamento=None))
        self.fields['cpf'] = forms.CharField(
            label='CPF:', max_length=11, required=False)


class EscolherAlunoDeclaracao(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EscolherAlunoDeclaracao, self).__init__(*args, **kwargs)
#        turma = forms.ModelChoiceField(queryset=Turma.objects.all())
    #    self.fields['turma'] = forms.ModelChoiceField(queryset=Turma.objects.all())
#        self.fields['turma'].queryset = forms.ModelChoiceField(queryset=Turma.objects.filter(instrutor=INSTRUTOR))

        self.fields['aluno'] = forms.ModelChoiceField(
            queryset=Aluno.objects.all(), required=False)
        self.fields['cpf'] = forms.CharField(
            label='CPF:', max_length=11, required=False)


class EscolherAlunoDeclaracao2(forms.Form):
    def __init__(self, aluno, *args, **kwargs):
        super(EscolherAlunoDeclaracao2, self).__init__(*args, **kwargs)
#        turma = forms.ModelChoiceField(queryset=Turma.objects.all())
    #    self.fields['turma'] = forms.ModelChoiceField(queryset=Turma.objects.all())
#        self.fields['turma'].queryset = forms.ModelChoiceField(queryset=Turma.objects.filter(instrutor=INSTRUTOR))

#        Turma
        print('aluno form: ', aluno)
        self.fields['aluno_turma'] = forms.ModelChoiceField(
            queryset=Aluno_Turma.objects.filter(aluno=aluno), required=False)


class login(forms.Form):
    username = forms.CharField(label='Usuário:', max_length=50)
    password = forms.CharField(
        label='Senha:', max_length=50, widget=forms.PasswordInput())


class Altera_Situacao(forms.Form):
    nome = forms.CharField(label='Aluno:', disabled=True,
                           max_length=100, required=False)
    situacao = forms.ModelChoiceField(
        widget=forms.Select, queryset=Situacao.objects.all())


class Altera_Situacao_Prevista(forms.Form):
    nome = forms.CharField(label='Aluno:', disabled=True,
                           max_length=100, required=False)
    situacao = forms.ModelChoiceField(
        widget=forms.Select, queryset=Status_Aluno_Turma_Prevista.objects.none())
    aluno_id = forms.IntegerField(disabled=True, required=False)


class Altera_Situacao_Prevista_Formset(BaseFormSet):
    def __init__(self, *args, QUERYSET, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.fields['situacao'].queryset = QUERYSET

# Tira as tags <li> do widget de checkbox para ele poder ser colocado na horizontal


class HorizontalCheckbox(forms.CheckboxSelectMultiple):
    def render(self, *args, **kwargs):
        output = super(HorizontalCheckbox, self).render(*args, **kwargs)
        return mark_safe(output.replace(u'<li>', u''))


class EscolherDia(forms.Form):
    data = forms.ChoiceField(widget=forms.Select)

    def __init__(self, *args, CHOICES, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data'].choices = CHOICES


class EscolherTurmaPrevista(forms.Form):
    turma = forms.ModelChoiceField(widget=forms.Select, queryset=None)

    def __init__(self, *args, QUERYSET, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['turma'].queryset = QUERYSET


class Controle_Presenca(forms.Form):
    nome = forms.CharField(label='Aluno:', disabled=True,
                           max_length=100, required=False)
    dias = forms.MultipleChoiceField(
        widget=HorizontalCheckbox(), required=False)
    #dia = forms.ChoiceField(widget=forms.CheckboxInput, label = '')

    def __init__(self, *args, CHOICES, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dias'].choices = CHOICES


class Confirmar_Turma(forms.Form):
    nome = forms.CharField(label='Turma:', disabled=True, required=False)
    confirma = forms.BooleanField(widget=forms.CheckboxInput, required=False)


class EscolherData(forms.Form):
    dt_inicio_i = forms.DateField(
        label='Data:', required=False, widget=forms.SelectDateWidget(years=range(2019, 2025)))
    dt_inicio_f = forms.DateField(
        label='Data:', required=False, widget=forms.SelectDateWidget(years=range(2019, 2025)))
    dt_fim_i = forms.DateField(label='Data:', required=False,
                               widget=forms.SelectDateWidget(years=range(2019, 2025)))
    dt_fim_f = forms.DateField(label='Data:', required=False,
                               widget=forms.SelectDateWidget(years=range(2019, 2025)))


class EscolherDataCad(forms.Form):
    dt_inicio = forms.DateField(label='Data Início:', required=False,
                                widget=forms.SelectDateWidget(years=range(2019, 2025)))
    dt_fim = forms.DateField(label='Data Fim:', required=False,
                             widget=forms.SelectDateWidget(years=range(2019, 2025)))


class CursoForm(ModelForm):
    turnos = forms.ModelMultipleChoiceField(
        queryset=Turno.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Turnos:"
    )

    class Meta:
        model = Curso
        exclude = ['dt_inclusao']
