from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, QueryDict
from django.forms.models import model_to_dict
from .forms import EscolherTurma, Altera_Situacao, Controle_Presenca, EscolherDia
from cevest.models import Curso, Aluno, Cidade, Bairro, Profissao, Escolaridade, Matriz, Turma_Prevista, Aluno_Turma, Turma, Situacao, Disciplina, Presenca, Feriado
import datetime
from .functions import get_proper_casing, compare_brazilian_to_python_weekday, convert_date_to_tuple, convert_tuple_to_data, create_select_choices, is_date_holiday,create_not_fixed_holidays_in_db
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
from django.urls import reverse
from django.forms.formsets import formset_factory
from .criarmatrizes import getCursos

@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def capitalizar_nomes(request):
    print(request.user)
    alunos = Aluno.objects.all()
    for aluno in alunos:
        aluno.nome = get_proper_casing(aluno.nome)
        aluno.save()
    return HttpResponseRedirect("/index")

@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def criar_feriados_moveis(request):
    current_year = datetime.date.today().year
    #print(type(current_year))
    #current_year = current_year.year
    for i in range(0,100):
        create_not_fixed_holidays_in_db(current_year+i)
    return HttpResponseRedirect("/index")

@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def AreaAdmin(request):
    return render(request,"Administracao/admin_area.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("index")

class temp_disciplina:
    nome = None
    numero_aulas = None
    numero_horas = None
    def __init__(self, nome, numero_aulas, numero_horas):
        self.nome = nome
        self.numero_aulas=numero_aulas
        self.numero_horas=numero_horas
        self.clean()
    def clean(self):
        if self.numero_aulas < 10:
            self.numero_aulas = "0" + str(self.numero_aulas)
        if self.numero_horas < 10:
            self.numero_horas = "0" + str(self.numero_horas)
    

@login_required
@permission_required('cevest.pode_emitir_certificado', raise_exception=True)
def SelecionarTurmaParaCertificado(request):
    if request.method == 'POST':
        turma = EscolherTurma(request.POST)   
        turma = request.POST.get("turma")
        request.session["turma"] = turma
        return HttpResponseRedirect(reverse('administracao:gerar_certificados'))
    form = EscolherTurma()
    return render(request,"Administracao/escolher_turma_nova_aba.html",{'form':form})

@login_required
@permission_required('cevest.pode_emitir_certificado', raise_exception=True)
def GerarCertificados(request):
    turma_id = request.session["turma"]
    turma = get_object_or_404(Turma,id=turma_id)
    aprovado = Situacao.objects.get(descricao = "aprovado")
    turma_aluno = Aluno_Turma.objects.filter(turma = turma,situacao=aprovado.id)
    alunos = []
    for ta in turma_aluno:
        alunos.append(ta.aluno)
    curso_turma = turma.curso
    data_inicio = turma.dt_inicio.strftime("%d/%m")
    data_fim = turma.dt_fim.strftime("%d/%m/%Y")
    data_atual = datetime.date.today()
    instrutor = turma.instrutor

    matrizes = Matriz.objects.filter(curso=curso_turma, curriculo = turma.curriculo)
    disciplinas = []
    total_horas = 0
    total_aulas = 0

    for mat in matrizes:
        disciplinas.append(temp_disciplina(mat.disciplina.nome,mat.num_aulas,mat.carga_horaria_total))
        total_horas = total_horas + mat.carga_horaria_total
        total_aulas = total_aulas + mat.num_aulas

    context = {
        'alunos' : alunos,
        'curso' : curso_turma,
        'turma' : turma,
        'data_inicio' : data_inicio,
        'data_fim' : data_fim,
        'data_atual' : data_atual,
        'instrutor' : instrutor,
        'disciplinas': disciplinas,
        'total_horas' : total_horas,
        'total_aulas': total_aulas,
    }

    template_name = 'Administracao/certificados.html'
    return render(request, template_name,context)

@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def SelecionarTurmaParaSituacao(request):
    if request.method == 'POST':
        turma = EscolherTurma(request.POST)   
        turma = request.POST.get("turma")
        request.session["turma"] = turma
        return HttpResponseRedirect(reverse('administracao:alterar_situacao_aluno'))
    form = EscolherTurma()
    return render(request,"Administracao/escolher_turma.html",{'form':form})

@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def AlterarSituacaoAluno(request):
    temp_turma = request.session["turma"]
    nome_turma = Turma.objects.get(id = temp_turma)
    turma_aluno = Aluno_Turma.objects.filter(turma = temp_turma)
    data = []
    for ta in turma_aluno:
        temp_dict = {"nome" : ta.aluno.nome, "situacao": ta.situacao.id}
        data.append(temp_dict)
    SituacaoFormset = formset_factory(Altera_Situacao,max_num=len(data))
    if request.method == "POST":
        post_data = request.POST.copy()
        formset = SituacaoFormset(post_data,data)
        i=0
        if formset.is_valid():
            for ta in turma_aluno:
                situacao_id = post_data.get('form-'+ str(i) +'-situacao')
                situacao_id = int(situacao_id)
                ta.situacao = Situacao.objects.get(id=situacao_id)
                ta.save()
                i = i+1
            return HttpResponseRedirect(reverse('administracao:area_admin'))
        else:
            print("Erro:")
            print(formset.errors)
    formset = SituacaoFormset(initial=data)
    return render(request,"Administracao/alterar_situacao.html",{'formset':formset, 'nome_turma':nome_turma})

@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def AdicionarMatrizesDeTxT(request):
    matrizes = getCursos("/home/cevest/public_html/pmnf/matrizes.txt")
    cursos_criados = []
    disciplinas_criadas = []
    for m in matrizes:
        curso_ = m['curso']
        disciplina_ = m['disciplina']
        num_aulas_ = m['número de aulas']
        carga_horaria_total_ = m['carga horária']

        curso_temp, created_curso = Curso.objects.get_or_create(
            nome = curso_
        )

        disciplina_temp, created_disciplina = Disciplina.objects.get_or_create(
            nome = disciplina_
        )

        if created_curso:
            cursos_criados.append(curso_)
        if created_disciplina:
            disciplinas_criadas.append(disciplina_)

        obj, created = Matriz.objects.get_or_create(
            curso = curso_temp,
            disciplina = disciplina_temp,
            num_aulas = num_aulas_,
            carga_horaria_total = carga_horaria_total_
        )
    return render(request,"Administracao/criar_matriz_txt.html", {"cursos_criados":cursos_criados, "disciplinas_criadas":disciplinas_criadas})

@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def SelecionarTurmaParaControle(request):
    if request.method == 'POST':
        turma = EscolherTurma(request.POST)   
        turma = request.POST.get("turma")
        request.session["turma"] = turma
        return HttpResponseRedirect(reverse('administracao:escolher_dia_controle'))
    form = EscolherTurma()
    return render(request,"Administracao/escolher_turma.html",{'form':form})

@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def EscolherDiaParaControle(request):
    #Pega informações
    temp_turma = request.session["turma"]
    temp_turma = Turma.objects.get(id=temp_turma)
    horarios = temp_turma.horario.all()
    
    data_verificacao = temp_turma.dt_inicio

    total_dias = 0
    dias_aula = []

    
    while data_verificacao<=temp_turma.dt_fim:
        for horario in horarios:
            if compare_brazilian_to_python_weekday(int(horario.dia_semana), data_verificacao.weekday()) and not is_date_holiday(data_verificacao):
                total_dias += 1
                dias_aula.append(data_verificacao)
        data_verificacao = data_verificacao + datetime.timedelta(days=1)
    

    choices = create_select_choices(dias_aula)
    choices.append((len(choices),"Todos"))

    if request.method == 'POST':
        temp_dia = EscolherDia(request.POST,CHOICES = choices)
        if temp_dia.is_valid():
            index_data = int(temp_dia.cleaned_data['data'])
            if index_data == len(choices)-1:
                request.session['data'] = convert_date_to_tuple(dias_aula)
            else:
                request.session['data'] = convert_date_to_tuple([dias_aula[index_data],])
            return HttpResponseRedirect(reverse('administracao:controle_presenca')) 
    form = EscolherDia(CHOICES = choices)
    return render(request, "Administracao/escolher_data.html", {"form" : form})

@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def ControleDePresenca(request):
    temp_turma = request.session["turma"]
    temp_dia = request.session["data"]
    temp_turma = Turma.objects.get(id=temp_turma)
    
    #arrumar isso depois
    dias_aula = convert_tuple_to_data(temp_dia)
    #Cria as opções de botões para o form
    choices = []
    i = 0
    for dia in dias_aula:
        choices.append((i,""))
        i+=1

    #Adquire os nomes dos alunos e as presenças já existentes e prepara para o form
    turma_aluno = Aluno_Turma.objects.filter(turma = temp_turma)
    initial_data = []
    for ta in turma_aluno:
        presenca = []
        temp_presenca = Presenca.objects.filter(turma = temp_turma, aluno = ta.aluno)
        for index in range(0,len(dias_aula)):
            for p in temp_presenca:
                if dias_aula[index]==p.data_aula and p.presente:
                    presenca.append(str(index))
        initial_data.append({'nome':ta.aluno.nome, 'dias':presenca})
    
    #cria o form
    formset_controle_presenca = formset_factory(Controle_Presenca,max_num = len(turma_aluno))
    formset = formset_controle_presenca(form_kwargs = {'CHOICES': choices},initial = initial_data)
    
    #Validação e salvar
    if request.method != 'POST':
        return render(request, "Administracao/controle_frequencia.html",{"formset" : formset, "data":dias_aula})
    temp_presenca = formset_controle_presenca(request.POST, form_kwargs = {'CHOICES': choices},initial = initial_data)
    if temp_presenca.is_valid():
        i=0
        for form in temp_presenca:
            print("Savou " + str(i))
            aluno = turma_aluno[i].aluno
            i+=1
            dias = form.cleaned_data['dias'] 
            for index in range(0,len(dias_aula)):
                if str(index) in dias:
                    temp_presenca_criada, created_presenca = Presenca.objects.get_or_create(turma = temp_turma, aluno = aluno, data_aula = dias_aula[index])
                    temp_presenca_criada.presente = True
                    temp_presenca_criada.save()
                else:
                    if Presenca.objects.filter(turma = temp_turma, aluno = aluno, data_aula = dias_aula[index],presente=True).count()>0:
                        temp_presenca_criada = Presenca.objects.get(turma = temp_turma, aluno = aluno, data_aula = dias_aula[index],presente=True)
                        temp_presenca_criada.presente = False
                        temp_presenca_criada.save()
    else:
        print(temp_presenca.errors)
    return HttpResponseRedirect(reverse('administracao:controle_frequencia'))

