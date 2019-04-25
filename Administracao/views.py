from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, QueryDict
from django.forms.models import model_to_dict
from .forms import EscolherTurma, Altera_Situacao
from cevest.models import Curso, Aluno, Cidade, Bairro, Profissao, Escolaridade, Matriz, Turma_Prevista, Aluno_Turma, Turma, Situacao, Disciplina
import datetime
from .functions import get_proper_casing
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
    return render(request,"Administracao/escolher_turma.html",{'form':form})

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
    matrizes = getCursos("/matrizes.txt")
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
