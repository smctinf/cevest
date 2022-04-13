from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, QueryDict
from django.forms.models import model_to_dict
from .forms import *
from cevest.models import Curso, Aluno, Cidade, Bairro, Profissao, Escolaridade, Matriz, Turma_Prevista, Aluno_Turma, Turma, Situacao, Disciplina, Presenca, Feriado, Situacao_Turma, Turma_Prevista_Turma_Definitiva, Aluno_Turma_Prevista, Status_Aluno_Turma_Prevista, Horario, Turno, Instrutor, User, Programa
from cevest.forms import CadForm
from cevest.views import getLista_Alocados, getLista_Candidatos, getLista_NaoAlocados
import datetime
from .functions import get_proper_casing, compare_brazilian_to_python_weekday, convert_date_to_tuple, convert_tuple_to_data, create_select_choices, is_date_holiday,create_not_fixed_holidays_in_db
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.forms.formsets import formset_factory
from .criarmatrizes import getCursos
from django.contrib import messages

#JLB
from django.db.models import Count, Q, Sum, Avg


@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def capitalizar_nomes(request):
    alunos = Aluno.objects.all()
    for aluno in alunos:
        aluno.nome = get_proper_casing(aluno.nome)
        aluno.save()
    messages.info(request,'Nomes Capitalizados')
    return HttpResponseRedirect("/index")

@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def criar_feriados_moveis(request):
    current_year = datetime.date.today().year
    for i in range(0,100):
        create_not_fixed_holidays_in_db(current_year+i)
    messages.info(request,'Feriados Móveis Criados')
    return HttpResponseRedirect("/index")

@login_required
# @permission_required('cevest.acesso_admin', raise_exception=True)
def AreaAdmin(request):
    return render(request,"Administracao/admin_area.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/administracao")


@login_required
# @permission_required('cevest.acesso_admin', raise_exception=True)
def tabelas(request):
    return render(request,"Administracao/tabelas.html")


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
@permission_required('Administracao.pode_emitir_certificado', raise_exception=True)
def SelecionarTurmaParaCertificado(request):
    if request.method == 'POST':
        turma = request.POST.get("turma")
        request.session["turma"] = turma
        cpf = request.POST.get("cpf")
        request.session["cpf"] = cpf

        return HttpResponseRedirect(reverse('administracao:gerar_certificados'))

    usuario = User.objects.get(username=request.user.username)
    if request.user.is_superuser:
        administrador = 's'
        INSTRUTOR = ''
    else:
        administrador = 'n'
        INSTRUTOR = Instrutor.objects.get(user=usuario)

    form = EscolherTurmaCertificado(administrador, INSTRUTOR)
    return render(request,"Administracao/escolher_turma_nova_aba.html",{'form':form})

@login_required
@permission_required('Administracao.pode_emitir_certificado', raise_exception=True)
def GerarCertificados(request):
    turma_id = request.session["turma"]
    turma = get_object_or_404(Turma,id=turma_id)
    aprovado = Situacao.objects.get(descricao = "aprovado")

    cpf = request.session["cpf"]

    if (cpf):
        try:
            aluno = Aluno.objects.get(cpf=cpf)
        except:
            print("Retorno de mais de um CPF!")
            aluno = ''

        if (aluno):
            turma_aluno = Aluno_Turma.objects.filter(turma = turma,situacao=aprovado.id,aluno=aluno)
        else:
            turma_aluno = []
    else:
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
#@permission_required('cevest.acesso_admin', raise_exception=True)
def SelecionarTurmaParaSituacao(request):
    if request.method == 'POST':
#        turma = EscolherTurma(request.POST)
        turma_aux = request.POST.get("turma")
        request.session["turma"] = turma_aux
        return HttpResponseRedirect(reverse('administracao:alterar_situacao_aluno'))

    usuario = User.objects.get(username=request.user.username)
    if request.user.is_superuser:
        administrador = 's'
        INSTRUTOR = ''
    else:
        administrador = 'n'
        INSTRUTOR = Instrutor.objects.get(user=usuario)
    # turma = EscolherTurma(request.POST)   

    form = EscolherTurma('s', administrador, INSTRUTOR)
    return render(request,"Administracao/escolher_turma.html",{'form':form})

@login_required
#@permission_required('cevest.acesso_admin', raise_exception=True)
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
            messages.info(request,'Situações Alteradas')
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
    messages.info(request,'Cursos Adicionados')
    return render(request,"Administracao/criar_matriz_txt.html", {"cursos_criados":cursos_criados, "disciplinas_criadas":disciplinas_criadas})

@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def SelecionarTurmaParaControle(request):
    if request.method == 'POST':
#        turma = EscolherTurma(request.POST)   
        turma = request.POST.get("turma")
        request.session["turma"] = turma
        return HttpResponseRedirect(reverse('administracao:escolher_dia_controle'))

    usuario = User.objects.get(username=request.user.username)
    if request.user.is_superuser:
        administrador = 's'
        INSTRUTOR = ''
    else:
        administrador = 'n'
        INSTRUTOR = Instrutor.objects.get(user=usuario)


    form = EscolherTurma('s', administrador, INSTRUTOR)
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
        messages.info(request,'Presenças Salvas')
    else:
        print(temp_presenca.errors)
    return HttpResponseRedirect(reverse('administracao:controle_presenca'))

@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def ArrumarSituacaoTurmaBacalhau(request):
    temp_relacao_turma = Turma_Prevista_Turma_Definitiva.objects.all()
    situacao_confirmada = Situacao_Turma.objects.get(descricao = "Confirmada")
    for turma in temp_relacao_turma:
        turma.turma_prevista.situacao = situacao_confirmada
        turma.turma_prevista.save()
    messages.info(request,'Situação de todas as turmas previstas mudada para confirmada')
    return HttpResponseRedirect(reverse('administracao:index'))

@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def ConfirmarTurma(request):
    situacao_aguardando = Situacao_Turma.objects.get(descricao = "Aguardando")
    situacao_confirmada = Situacao_Turma.objects.get(descricao = "Confirmada")
    temp_turmas = Turma_Prevista.objects.filter(situacao = situacao_aguardando)
    temp_status_aluno = Status_Aluno_Turma_Prevista.objects.get(descricao = "Matriculado")
    temp_aluno_turma_prevista = []

    initial_data = []
    for turma in temp_turmas:
        initial_data.append({'nome':turma})
    formset_confirmar_turma = formset_factory(Confirmar_Turma,max_num = len(temp_turmas))
    formset = formset_confirmar_turma(initial = initial_data)

    if request.method == 'POST':
        temp_turmas_confirmadas = formset_confirmar_turma(request.POST, initial = initial_data)
        if temp_turmas_confirmadas.is_valid():
            i = 0
            for form in temp_turmas_confirmadas:
                if form.cleaned_data['confirma']:
                    temp_turmas[i].situacao = situacao_confirmada                    
                    temp_turma_criada,created_turma = Turma.objects.get_or_create(
                        nome = temp_turmas[i].nome,
                        curso = temp_turmas[i].curso,
                        curriculo = temp_turmas[i].curriculo,
                        instrutor = temp_turmas[i].instrutor,
                        dt_inicio = temp_turmas[i].dt_inicio,
                        dt_fim = temp_turmas[i].dt_fim,
                        quant_alunos = temp_turmas[i].quant_alunos
                    )
                    
                    if created_turma:
                        temp_turma_criada.horario.set(temp_turmas[i].horario.all())
                        temp_aluno_turma_prevista = Aluno_Turma_Prevista.objects.filter(turma_prevista = temp_turmas[i], status_aluno_turma_prevista = temp_status_aluno)
                        for aluno_turma_relacao in temp_aluno_turma_prevista:
                            temp_aluno_turma = Aluno_Turma.objects.create(turma = temp_turma_criada, aluno = aluno_turma_relacao.aluno)
                            #temp_aluno_turma.save()

                    relacao_turmas, created_relacao = Turma_Prevista_Turma_Definitiva.objects.get_or_create(
                        turma_prevista = temp_turmas[i],
                        turma = temp_turma_criada
                        )
                    
                    temp_turmas[i].save()
                    temp_turma_criada.save()
                    relacao_turmas.save()
                i+=1
            messages.info(request,'Turmas Confirmadas')
        else:
            print(temp_turmas_confirmadas.errors)
        return HttpResponseRedirect(reverse('administracao:confirmar_turma'))
    return render(request, "Administracao/confirmar_turma.html",{"formset" : formset})

@login_required
@permission_required('cevest.pode_fazer_alocacao', raise_exception=True)
def EscolherTurmaPrevistaParaAlocacao(request):
    situacao_cancelada = Situacao_Turma.objects.get(descricao = "Cancelada")
    turmas_previstas = Turma_Prevista.objects.exclude(situacao = situacao_cancelada)
    turmas_previstas = turmas_previstas.exclude(dt_fim__lt = datetime.date.today())

    if request.method == 'POST':
        form = EscolherTurmaPrevista(request.POST, QUERYSET = turmas_previstas)
        if form.is_valid():
            request.session['turma_prevista_id'] = form.cleaned_data['turma'].id
            return HttpResponseRedirect(reverse('administracao:alocacao'))

    form = EscolherTurmaPrevista(QUERYSET = turmas_previstas)
    return render(request,"Administracao/escolher_turma.html",{'form':form})

@login_required
@permission_required('cevest.pode_fazer_alocacao', raise_exception=True)
def Alocacao(request):
    #Ordem de prioridade:
    #1-Ordem judicial
    #2-Necessidades Especiais
    #----
    #3-Bolsa família
    #4-Programas sociais
    #5-Desempregado
    #6-Filhos
    #7-Idade

    turma_prevista_id = request.session['turma_prevista_id']
    turma_prevista = Turma_Prevista.objects.get(id = turma_prevista_id)

    horario_manha = Turno.objects.get(descricao = "Manhã")
    horario_tarde = Turno.objects.get(descricao = "Tarde")
    horario_noite = Turno.objects.get(descricao = "Noite")

    # ============== ALTERACAO PARA PEGAR Só A PARTIR DE NOVEMBRO

#    alunos_compativeis = Aluno.objects.filter(cursos = turma_prevista.curso).filter(ativo=True).filter(dt_inclusao__gt='2022-02-08').filter(dt_inclusao__lt='2022-02-09')
    alunos_compativeis = Aluno.objects.filter(cursos = turma_prevista.curso).filter(ativo=True).filter(dt_inclusao__gt='2021-11-01')
#    alunos_compativeis = Aluno.objects.filter(cursos = turma_prevista.curso).filter(ativo=True)

    lista_final = []
    
    turma_prevista_alunos = Aluno_Turma_Prevista.objects.filter(turma_prevista = turma_prevista)

    #Exclui de alunos compativeis os alunos q já estão na lista ta turma
    for tmp_turma_prevista_alunos in turma_prevista_alunos:
        alunos_compativeis = alunos_compativeis.exclude(id = tmp_turma_prevista_alunos.aluno_id)

    status_candidato = Status_Aluno_Turma_Prevista.objects.get(descricao = "Candidato")
    status_matriculado = Status_Aluno_Turma_Prevista.objects.get(descricao = "Matriculado")
    
    #exclui alunos já matriculados ou já selecionados, sobrando os que desistiram da vaga ou não compareceram

    turma_prevista_alunos = turma_prevista_alunos.exclude(status_aluno_turma_prevista = status_matriculado).exclude(status_aluno_turma_prevista = status_candidato)

    #pega os alunos com horários disponíveis compatíveis com o curso.

    if len(turma_prevista.horario.filter(hora_inicio = datetime.time(hour = 8, minute = 00 ))) > 0:
        alunos_compativeis = alunos_compativeis.filter(disponibilidade = horario_manha)

    if len(turma_prevista.horario.filter(hora_inicio = datetime.time(hour = 13))) > 0:
        alunos_compativeis = alunos_compativeis.filter(disponibilidade = horario_tarde)

    if len(turma_prevista.horario.filter(hora_inicio = datetime.time(hour = 18))) > 0:
        alunos_compativeis = alunos_compativeis.filter(disponibilidade = horario_noite)


    # Exclui de alunos_compativeis os alunos que desistiram da vaga ou não compareceram

    for aluno_turma in turma_prevista_alunos:
        alunos_compativeis = alunos_compativeis.exclude(id = aluno_turma.aluno.id)

    for aluno in alunos_compativeis:

        # Verifica se aluno já foi selecionado para este curso. Caso positivo, exclui

        alunos_temp = Aluno_Turma_Prevista.objects.filter(aluno = aluno)

        for aluno_temp in alunos_temp:
            if aluno_temp.turma_prevista.curso == turma_prevista.curso:
                alunos_compativeis = alunos_compativeis.exclude(id = aluno.id)
                continue


        aluno_turma = Aluno_Turma.objects.filter(aluno = aluno)
        for turma_aluno in aluno_turma:

            # Verifica se aluno já cursou este curso. Caso positivo, exclui

            alunos_temp = Aluno_Turma.objects.filter(aluno = aluno)

            for aluno_temp in alunos_temp:
                if aluno_temp.turma.curso == turma_prevista.curso:
                    alunos_compativeis = alunos_compativeis.exclude(id = aluno.id)
                    continue

            if turma_aluno.turma.dt_fim < turma_prevista.dt_inicio:
                continue
            if turma_prevista.dt_fim < turma_aluno.turma.dt_inicio:
                continue

            # Verifica se horário conflita

            for horario in turma_aluno.turma.horario.all():
                if horario in turma_prevista.horario.all():
                    print("aluno removido da lista por conflito de horário:" + str(aluno))
                    alunos_compativeis = alunos_compativeis.exclude(id = aluno.id)


    #O sistema de pontos é definido de modo que a pessoa que tem uma prioridade maior que outra sempre receba
    #mais pontos. Por exemplo, portadores de necessidade especiais recebem 16 pontos no mínimo, e pessoas com
    #bolsa família, a prioridade imediatamente abaixo, podem receber no máximo 15 pontos. Assim, a quantidade
    #de pontos para cada prioridade precisa ser uma potência de 2 (1,2,4,8,16,etc.) com a prioridade maior
    #tendo mais pontos.

    #Colocar p+=1 antes de checar cada condição, do jeito que está o código abaixo, permite definir a prioridade
    #de cada condição apenas pela ordem de verificação, sendo que a primeira condição a ser verificada tem 
    #prioridade menor que as seguintes.

    for aluno in alunos_compativeis:

        # Verifica se já fez outro curso
        aluno_turma_temp = Aluno_Turma.objects.filter(aluno = aluno)

        if len(aluno_turma_temp) == 0:
            ja_fez_curso = 0
        else:
            ja_fez_curso = 2
            for x in aluno_turma_temp:
                if x.situacao_id == 2 or x.situacao_id == 6:
                    ja_fez_curso = 1
                    break


        # Verifica se já foi selecionado para algum curso

        # 0: Nunca foi selecionado para curso nenhum
        # 1: já fez curso, consequentemente já esteve matriculado em uma turma prevista
        # 2: Não compareceu
        # 3: Está como candidato

        aluno_turma_prevista_temp = Aluno_Turma_Prevista.objects.filter(aluno = aluno)
        if len(aluno_turma_prevista_temp) == 0:
            if ja_fez_curso == 1:
                ja_foi_selecionado = 1
            else:
                ja_foi_selecionado = 0

        else:
            ja_foi_selecionado = 2
            for x in aluno_turma_prevista_temp:
                if x.status_aluno_turma_prevista_id == 1:
                    ja_foi_selecionado = 3
                    break

            if ja_foi_selecionado == 2:
                for x in aluno_turma_prevista_temp:
                    if x.status_aluno_turma_prevista_id == 2 or x.status_aluno_turma_prevista_id == 4:
                        ja_foi_selecionado = 1
                        break

    

        temp_pontuacao = 0
        p = 0
        if aluno.quant_filhos > 0:
            temp_pontuacao += 2**p
        p += 1
        if aluno.desempregado:
            temp_pontuacao += 2**p
        p += 1
        if aluno.nis:
            temp_pontuacao += 2**p
        p += 1
        if aluno.bolsa_familia:
            temp_pontuacao += 2**p

        # Se curso tradicional, entre os que já fizeram curso, maior prioridade para quem concluiu ou justificou
        if turma_prevista.curso.programa_id == 1:
            p += 1
            if ja_fez_curso == 1:
                temp_pontuacao += 2**p

        # Dependendo do programa a q o curso pertence, terá prioridade diferenciada
        p += 1
        if ja_fez_curso == 1 and turma_prevista.curso.programa_id == 2:
            temp_pontuacao += 2**p
        else:
            if ja_foi_selecionado == 0 and turma_prevista.curso.programa_id == 1:
                temp_pontuacao += 2**p
        #
        p += 1
        if aluno.portador_necessidades_especiais:
            temp_pontuacao += 2**p
        p += 1
        if aluno.ordem_judicial:
            temp_pontuacao += 2**p
        # Se já foi selecionado para algum curso, e está como candidato, tem prioridade mínima
        p += 1
        if ja_foi_selecionado != 3:
            temp_pontuacao += 2**p

        temp_dict = {"aluno":aluno,"pontuação":temp_pontuacao,"dt_nasc":aluno.dt_nascimento,'dt_inclusao':aluno.dt_inclusao,'situacao':Status_Aluno_Turma_Prevista.objects.none()}
        lista_final.append(temp_dict)

        if aluno.dt_nascimento == '' or aluno.dt_inclusao == '':
            exit
        # else:
        #    print ('Aluno ok: ', aluno.nome)

    lista_final = sorted(lista_final, key = lambda i: (-i['pontuação'],i['dt_inclusao'],i['dt_nasc']))

    
    quant_na_turma = Aluno_Turma_Prevista.objects.filter(turma_prevista=turma_prevista).filter(status_aluno_turma_prevista=status_candidato).count()
    quant_na_turma += Aluno_Turma_Prevista.objects.filter(turma_prevista=turma_prevista).filter(status_aluno_turma_prevista=status_matriculado).count()

    i = quant_na_turma

    for aluno_pontuacao in lista_final:
        if(i >= turma_prevista.quant_alunos):
            break

        temp_aluno_turma_prevista,created = Aluno_Turma_Prevista.objects.get_or_create(
            aluno = aluno_pontuacao['aluno'],
            turma_prevista = turma_prevista,
        )
        aluno_pontuacao['situacao'] = temp_aluno_turma_prevista.status_aluno_turma_prevista

        i+=1

    i = turma_prevista.quant_alunos - quant_na_turma

    lista_selecionados = lista_final[0:i]
    lista_nao_selecionados = lista_final[i:]

    return render(request,"Administracao/alocacao.html",{'nome_turma':turma_prevista,'alocados':lista_selecionados,"nao_alocados":lista_nao_selecionados,"nao_considerados":turma_prevista_alunos})

@login_required
#@permission_required('cevest.acesso_admin', raise_exception=True)
@permission_required('Administracao.pode_emitir_certificado', raise_exception=True)
def EscolherTurmaPrevistaParaAlterarSituacao(request):
    situacao_cancelada = Situacao_Turma.objects.get(descricao = "Cancelada")
    turmas_previstas = Turma_Prevista.objects.exclude(situacao = situacao_cancelada)
    turmas_previstas = turmas_previstas.exclude(dt_fim__lt = datetime.date.today())

    if request.method == 'POST':
        form = EscolherTurmaPrevista(request.POST, QUERYSET = turmas_previstas)
        if form.is_valid():
            request.session['turma_prevista_id'] = form.cleaned_data['turma'].id
            return HttpResponseRedirect(reverse('administracao:alterar_situacao_turma_prevista'))

    form = EscolherTurmaPrevista(QUERYSET = turmas_previstas)
    return render(request,"Administracao/escolher_turma.html",{'form':form})

@login_required
#@permission_required('cevest.acesso_admin', raise_exception=True)
@permission_required('Administracao.pode_emitir_certificado', raise_exception=True)
def AlterarSituacaoTurmaPrevista(request):
    situacao_matriculado = Status_Aluno_Turma_Prevista.objects.get(descricao = "Matriculado")
    situacoes_nao_matriculados = Status_Aluno_Turma_Prevista.objects.exclude(descricao = "Matriculado")
    #situacoes_nao_candidatos_ou_matriculados = Status_Aluno_Turma_Prevista.objects.exclude(descricao = "Matriculado").exclude(descricao = "Candidato")
    situacao_candidato = Status_Aluno_Turma_Prevista.objects.get(descricao = "Candidato")

    turma_prevista_id = request.session['turma_prevista_id']
    turma_prevista = Turma_Prevista.objects.get(id = turma_prevista_id)
    aluno_turma_prevista = Aluno_Turma_Prevista.objects.filter(turma_prevista = turma_prevista)
    aluno_turma_prevista_candidato = aluno_turma_prevista.filter(status_aluno_turma_prevista = situacao_candidato)
    aluno_turma_prevista_matriculado = aluno_turma_prevista.filter(status_aluno_turma_prevista = situacao_matriculado)
    aluno_turma_prevista_nao_matriculado = aluno_turma_prevista.exclude(status_aluno_turma_prevista = situacao_candidato).exclude(status_aluno_turma_prevista = situacao_matriculado)


    data_matriculados = []
    for ta in aluno_turma_prevista_matriculado:
        temp_dict = {"nome" : ta.aluno.nome, "situacao": ta.status_aluno_turma_prevista.id, "aluno_id":ta.aluno.id}
        data_matriculados.append(temp_dict)
    data_matriculados = sorted(data_matriculados, key = lambda i: (i['situacao'],i['nome']))

    data_candidatos = []
    for ta in aluno_turma_prevista_candidato:
        temp_dict = {"nome" : ta.aluno.nome, "situacao": ta.status_aluno_turma_prevista.id, "aluno_id":ta.aluno.id}
        data_candidatos.append(temp_dict)
    data_candidatos = sorted(data_candidatos, key = lambda i: (i['situacao'],i['nome']))

    data_nao_matriculados = []
    for ta in aluno_turma_prevista_nao_matriculado:
        temp_dict = {"nome" : ta.aluno.nome, "situacao": ta.status_aluno_turma_prevista.id, "aluno_id":ta.aluno.id}
        data_nao_matriculados.append(temp_dict)
    data_nao_matriculados = sorted(data_nao_matriculados, key = lambda i: (i['situacao'],i['nome']))

    SituacaoFormset = formset_factory(form = Altera_Situacao_Prevista, formset = Altera_Situacao_Prevista_Formset, max_num=0)

    if request.method == "POST":
        post_data = request.POST.copy()
        formset_candidatos = SituacaoFormset(post_data,initial = data_candidatos,QUERYSET = situacoes_nao_matriculados, prefix = "candidatos")
        formset_matriculados = SituacaoFormset(post_data,initial = data_matriculados,QUERYSET = Status_Aluno_Turma_Prevista.objects.all(), prefix = "matriculados")
        formset_nao_matriculados = SituacaoFormset(post_data,initial = data_nao_matriculados,QUERYSET = situacoes_nao_matriculados, prefix = "nao_matriculados")

        if formset_candidatos.is_valid() and formset_matriculados.is_valid() and formset_nao_matriculados.is_valid():
            for form in formset_candidatos:
                id = form.cleaned_data['aluno_id']
                aluno_turma_temp = Aluno_Turma_Prevista.objects.get(turma_prevista = turma_prevista,aluno = form.cleaned_data['aluno_id'])
                aluno_turma_temp.status_aluno_turma_prevista = form.cleaned_data['situacao']
                aluno_turma_temp.save()
            for form in formset_matriculados:
                id = form.cleaned_data['aluno_id']
                aluno_turma_temp = Aluno_Turma_Prevista.objects.get(turma_prevista = turma_prevista,aluno = form.cleaned_data['aluno_id'])
                aluno_turma_temp.status_aluno_turma_prevista = form.cleaned_data['situacao']
                aluno_turma_temp.save()
            for form in formset_nao_matriculados:
                id = form.cleaned_data['aluno_id']
                aluno_turma_temp = Aluno_Turma_Prevista.objects.get(turma_prevista = turma_prevista,aluno = form.cleaned_data['aluno_id'])
                aluno_turma_temp.status_aluno_turma_prevista = form.cleaned_data['situacao']
                aluno_turma_temp.save()
            
            messages.info(request,'Situações Alteradas')
            return HttpResponseRedirect(reverse('administracao:alterar_situacao_turma_prevista'))
        else:
            print("Erro:")
            print(formset_candidatos.errors)

    formset_candidatos = SituacaoFormset(QUERYSET = situacoes_nao_matriculados,initial=data_candidatos, prefix = "candidatos")
    formset_matriculados = SituacaoFormset(QUERYSET = Status_Aluno_Turma_Prevista.objects.all(), initial=data_matriculados, prefix = "matriculados")
    formset_nao_matriculados = SituacaoFormset(QUERYSET = situacoes_nao_matriculados,initial = data_nao_matriculados, prefix = "nao_matriculados")
    return render(request,"Administracao/alterar_situacao_alunos_turma_prevista.html",{'formset_candidatos':formset_candidatos, 'formset_matriculados':formset_matriculados, 'formset_nao_matriculados':formset_nao_matriculados, 'nome_turma':turma_prevista})

@login_required
#@permission_required('cevest.acesso_admin', raise_exception=True)
@permission_required('Administracao.pode_emitir_certificado', raise_exception=True)
def ConfirmarInformacoesAlunoPrevisto(request,aluno_id,turma_id):
    turma_prevista = Turma_Prevista.objects.get(id = turma_id)
    aluno = get_object_or_404(Aluno,id=aluno_id)
    situacao_matriculado = Status_Aluno_Turma_Prevista.objects.get(descricao = "Matriculado")
    checked_curso_ids = []
    for curso in aluno.cursos.all():
        checked_curso_ids.append(curso.id)

    if request.method == 'POST':
        post_data = request.POST
        form = CadForm(post_data, instance = aluno)
        if form.is_valid():
            form.save(aluno)
            if "_salvar" in post_data:
                messages.info(request,'Cadastro Salvo')
            elif "_cadastrar" in post_data:
                #####
                aluno_turma = Aluno_Turma_Prevista.objects.filter(aluno = aluno).exclude(turma_prevista = turma_prevista)
                aluno_turma = aluno_turma.filter(status_aluno_turma_prevista = situacao_matriculado)
                for turma_aluno in aluno_turma:
                    if turma_aluno.turma_prevista.dt_fim < turma_prevista.dt_inicio:
                        continue
                    if turma_prevista.dt_fim < turma_aluno.turma_prevista.dt_inicio:
                        continue
                    for horario in turma_aluno.turma_prevista.horario.all():
                        if horario in turma_prevista.horario.all():
                            messages.info(request,'Conflito de horário com a turma ' + str(turma_aluno.turma_prevista))
                            return HttpResponseRedirect(reverse('administracao:area_admin'))
                #####
                ConfirmarAluno(request,aluno_id,turma_id)
#            return HttpResponseRedirect(reverse('administracao:area_admin'))
            return HttpResponseRedirect(reverse('administracao:alterar_situacao_turma_prevista'))
        else:
            print('Erro: ', form.errors)
            erro_tmp = str(form.errors)
            erro_tmp = erro_tmp.replace('<ul class="errorlist">', '')
            erro_tmp = erro_tmp.replace('</li>', '')
            erro_tmp = erro_tmp.replace('<ul>', '')
            erro_tmp = erro_tmp.replace('</ul>', '')

            erro_tmp = erro_tmp.split('<li>')

            messages.error(request, erro_tmp[1] + ': ' + erro_tmp[2])


    # Lista cursos separados por programas
    programas = Programa.objects.all().order_by('-nome')

    cursos = []

    for programa in programas:
        cursos_pgm = Curso.objects.filter(programa=programa).filter(exibir=True).filter(ativo=True)
        cursos.append({'programa': programa, 'cursos': cursos_pgm})


    form=CadForm(initial={'cidade':aluno.bairro.cidade,'cpf':aluno.cpf}, instance=aluno)

    return render(request,"Administracao/corrigir_cadastro.html",{'form':form, 'checked_curso_ids':checked_curso_ids, 'cursos':cursos})

def ConfirmarAluno(request,aluno_id,turma_id):
    turma_prevista = Turma_Prevista.objects.get(id = turma_id)
    aluno = get_object_or_404(Aluno,id=aluno_id)

    aluno_turma_prevista = Aluno_Turma_Prevista.objects.get(aluno = aluno, turma_prevista = turma_prevista)
    status_confirma = Status_Aluno_Turma_Prevista.objects.get(descricao = "Matriculado")

    if len(Turma_Prevista_Turma_Definitiva.objects.filter(turma_prevista = turma_prevista))>0:
        turma_definitiva_turma_prevista = Turma_Prevista_Turma_Definitiva.objects.get(turma_prevista = turma_prevista)
        aluno_turma, created = Aluno_Turma.objects.get_or_create(turma = turma_definitiva_turma_prevista.turma, aluno = aluno)
        aluno_turma.save()

    aluno_turma_prevista.status_aluno_turma_prevista = status_confirma
    aluno_turma_prevista.save()

    messages.info(request,'Cadastro Salvo')
    return HttpResponseRedirect(reverse('administracao:area_admin'))


@login_required
# @permission_required('Administracao.pode_emitir_certificado', raise_exception=True)
@permission_required('cevest.pode_fazer_alocacao', raise_exception=True)
def lista_alocados_telefone(request):
    lista_turmas = getLista_Alocados()
    return render(request, "cevest/lista_alocados_telefone.html",{"listas":lista_turmas})


@login_required
# @permission_required('Administracao.pode_emitir_certificado', raise_exception=True)
@permission_required('cevest.pode_fazer_alocacao', raise_exception=True)
def lista_alocados_telefone_zap(request):
    
#    lista_turmas = Aluno_Turma_Prevista.objects.filter(status_aluno_turma_prevista_id='1')
    # Alterado para gerar para todos os alunos
    lista_turmas = Aluno.objects.filter(ativo=True)
    return render(request, "Administracao/lista_alocados_telefone_zap.html",{"listas":lista_turmas})


@login_required
@permission_required('cevest.pode_fazer_alocacao', raise_exception=True)
def lista_alfabetica(request):
    lista_alfabetica = getLista_Candidatos()
    return render(request, "Administracao/lista_alfabetica.html",{"listas":lista_alfabetica}) 
"""
@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def lista_alfabetica(request):
    lista_alfabetica = getLista_Candidatos()
    return render(request, "Administracao/lista_alfabetica.html",{"listas":lista_alfabetica}) 
"""
@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def lista_nao_alocados(request):
    lista = getLista_NaoAlocados()
    return render(request, "Administracao/lista_nao_alocados.html",{"listas":lista}) 


@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def lista_todos_por_curso_e_turno(request, curso_id, turno_id):
    alunos = Aluno.objects.filter(cursos=curso_id, disponibilidade=turno_id)
    return render(request, "Administracao/lista_todos_por_curso_e_turno.html",{"alunos":alunos}) 


# Mostra quantidade de alunos que abandonaram ou cancelaram a matrícula em uma turma definitiva
@login_required
@permission_required('cevest.pode_fazer_alocacao', raise_exception=True)
def quantidade_situacao_aluno_turma(request):

    if request.method == 'POST':

        form = EscolherData(request.POST)
        if form.is_valid():

            dt_inicio_i = form.cleaned_data['dt_inicio_i']
            dt_inicio_f = form.cleaned_data["dt_inicio_f"]
            dt_fim_i = form.cleaned_data["dt_fim_i"]
            dt_fim_f = form.cleaned_data["dt_fim_f"]

        if dt_inicio_i == None:
            dt_inicio_i = '2019-01-01'

        if dt_inicio_f == None:
            dt_inicio_f = '2030-12-31'

        if dt_fim_i == None:
            dt_fim_i = '2019-01-01'

        if dt_fim_f == None:
            dt_fim_f = '2030-12-31'

        turmas = Turma.objects.filter(dt_inicio__gte=dt_inicio_i).filter(dt_inicio__lte=dt_inicio_f).filter(dt_fim__gte=dt_fim_i).filter(dt_fim__lte=dt_fim_f)
        situacoes = Situacao.objects.all()

        ###    turmas = turmas.annotate(turma_count = Count('aluno_turma', filter=Q(aluno_turma__situacao=1)))
        lista = []

        for turma in turmas:
            lista_tmp = []
            lista_tmp.append(turma.curso.nome)
            lista_tmp.append(turma.nome)
            for situacao in situacoes:
                lista_tmp.append(Aluno_Turma.objects.filter(situacao=situacao, turma=turma).count())

            lista.append(lista_tmp)

        # Calcula total
        tot2 = 0
        tot3 = 0
        tot4 = 0
        tot5 = 0
        tot6 = 0
        tot7 = 0

        for l in lista:
            tot2 += l[2]
            tot3 += l[3]
            tot4 += l[4]
            tot5 += l[5]
            tot6 += l[6]
            tot7 += l[7]

        total = [tot2, tot3, tot4, tot5, tot6, tot7]
        #    lista = sorted(lista, key = lambda i: (-i[2]))

        return render(request, "Administracao/quantidade_situacao_aluno_turma.html",{"lista":lista, "situacoes":situacoes, "total":total})

    else:
        form = EscolherData()
        return render(request,"Administracao/escolher_data_curso.html",{'form':form})


# Mostra quantidade de alunos por situação em uma turma prevista
@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def quantidade_situacao_aluno_turma_prevista(request):

    if request.method == 'POST':

        form = EscolherData(request.POST)
        if form.is_valid():

            dt_inicio_i = form.cleaned_data['dt_inicio_i']
            dt_inicio_f = form.cleaned_data["dt_inicio_f"]
            dt_fim_i = form.cleaned_data["dt_fim_i"]
            dt_fim_f = form.cleaned_data["dt_fim_f"]

        if dt_inicio_i == None:
            dt_inicio_i = '2019-01-01'

        if dt_inicio_f == None:
            dt_inicio_f = '2030-12-31'

        if dt_fim_i == None:
            dt_fim_i = '2019-01-01'

        if dt_fim_f == None:
            dt_fim_f = '2030-12-31'

        #    turmas = Turma.objects.filter(dt_inicio__gte=dt_inicio_i).filter(dt_inicio__lte=dt_inicio_f).filter(dt_fim__gte=dt_fim_i).filter(dt_fim__lte=dt_fim_f)

        turmas_previstas = Turma_Prevista.objects.exclude(situacao='3').filter(dt_inicio__gte=dt_inicio_i).filter(dt_inicio__lte=dt_inicio_f).filter(dt_fim__gte=dt_fim_i).filter(dt_fim__lte=dt_fim_f)

        status_aluno_turma_prevista = Status_Aluno_Turma_Prevista.objects.all()

        #    turmas_previstas = turmas_previstas.annotate(turma_count = Count('aluno_turma_prevista', filter=Q(aluno_turma_prevista__status_aluno_turma_prevista=0)))
        lista = []

        for turma_prevista in turmas_previstas:
            lista_tmp = []
            lista_tmp.append(turma_prevista.curso.nome)
            lista_tmp.append(turma_prevista.nome)

            lista_tmp.append(turma_prevista.quant_alunos)


            for status in status_aluno_turma_prevista:

        #            if status == status_aluno_turma_prevista[0]:
        #                lista_tmp.append(turma_prevista.turma_count)
        #            else:
                lista_tmp.append(Aluno_Turma_Prevista.objects.filter(status_aluno_turma_prevista=status, turma_prevista=turma_prevista).count())

            lista.append(lista_tmp)

        # Calcula total
        tot2 = 0
        tot3 = 0
        tot4 = 0
        tot5 = 0
        tot6 = 0

        for l in lista:
            tot2 += l[2]
            tot3 += l[3]
            tot4 += l[4]
            tot5 += l[5]
            tot6 += l[6]

        total = [tot2, tot3, tot4, tot5, tot6]

        #    lista = sorted(lista, key = lambda i: (-i[2]))

        return render(request, "Administracao/quantidade_situacao_aluno_turma_prevista.html",{"lista":lista, "status":status_aluno_turma_prevista, "total":total})

    else:
        form = EscolherData()
        return render(request,"Administracao/escolher_data_curso.html",{'form':form})


# Mostra lista de alunos "Cursando" em turmas encerradas até uma data
@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def alunos_formados_tel(request):
    situacao = Situacao.objects.get(descricao='Aprovado')
    alunos_turmas = Aluno_Turma.objects.filter(turma__dt_fim__lte='2019-07-14',situacao=situacao)
#    alunos_turmas = Aluno_Turma.objects.filter(turma__dt_fim__lte='2019-07-01')
    return render(request, "Administracao/alunos_formados_tel.html",{"alunos_turmas":alunos_turmas})

@login_required
def ajuda(request):
    return render(request,"Administracao/ajuda.html")

@login_required
def ajuda_funcionamento(request):
    return render(request,"Administracao/ajuda_funcionamento.html")

@login_required
def ajuda_atualizacoes(request):
    return render(request,"Administracao/ajuda_atualizacoes.html")


# Lista alunos com seus celulares por turma
@login_required
def lista_celular_por_turma(request, turma_aberta):
    if request.method == 'POST':

        turma_id = request.POST.get("turma")
        turma = Turma.objects.get(pk=turma_id)

        alunos_turmas = Aluno_Turma.objects.filter(turma=turma_id)
        return render(request,"Administracao/lista_celular_por_turma.html",{'alunos_turmas':alunos_turmas, 'turma':turma})


    # TODO: Colocar aqui para imprimir quem também tiver permissão de ver todas as turmas
    usuario = User.objects.get(username=request.user.username)

    if request.user.has_perm('Administracao.pode_emitir_certificado'):
        administrador = 's'
        INSTRUTOR = ''

    if request.user.is_superuser:
        administrador = 's'
        INSTRUTOR = ''
    else:

        if request.user.has_perm('Administracao.pode_emitir_certificado'):
            administrador = 's'
            INSTRUTOR = ''
        else:
            administrador = 'n'
            INSTRUTOR = Instrutor.objects.get(user=usuario)


    form = EscolherTurma(turma_aberta, administrador, INSTRUTOR)
    return render(request,"Administracao/escolher_lista_celular_por_turma.html",{'form':form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Senha alterada.')
            return redirect('/Administracao/change_password')
        else:
            messages.error(request, 'Corrigir o erro apresentado.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Administracao/change_password.html', {
        'form': form
    })


# Selecionar aluno para declaração
@login_required
@permission_required('Administracao.pode_emitir_certificado', raise_exception=True)
def SelecionarAlunoParaDeclaracao(request):
    if request.method == 'POST':
        aluno = request.POST.get("aluno")
        request.session["aluno"] = aluno
        cpf = request.POST.get("cpf")
        request.session["cpf"] = cpf

        return HttpResponseRedirect(reverse('administracao:gerar_declaracao'))

    form = EscolherAlunoDeclaracao()
    return render(request,"Administracao/escolher_aluno_nova_aba.html",{'form':form})


# Emitir declaração
@login_required
@permission_required('Administracao.pode_emitir_certificado', raise_exception=True)
def GerarDeclaracao(request):

    if request.method == 'POST':
        aluno_turma = request.POST.get("aluno_turma")

#        request.session["aluno"] = aluno
#        cpf = request.POST.get("cpf")
#        request.session["cpf"] = cpf

#        print ('aluno_turma: ', aluno_turma)

        if not aluno_turma:
            messages.info(request,'Aluno não consta em nenhum curso.')
            form = EscolherAlunoDeclaracao()
            return render(request,"Administracao/escolher_aluno_nova_aba.html",{'form':form})


        aluno_turma = get_object_or_404(Aluno_Turma,id=aluno_turma)

        aluno = get_object_or_404(Aluno,id=aluno_turma.aluno_id)

        aprovado = Situacao.objects.get(descricao = "Aprovado")
        cursando = Situacao.objects.get(descricao = "Cursando")


        if aluno_turma.situacao != aprovado and aluno_turma.situacao != cursando:
            messages.info(request,'Aluno não concluiu o curso. ')

            context = {
                'aluno' : aluno,
                'form':EscolherAlunoDeclaracao2(aluno),
            }

            return render(request, "Administracao/declaracao.html", context)

        turma = get_object_or_404(Turma,id=aluno_turma.turma_id)

        temp_horario = []

        for horario in turma.horario.all():

            if horario.dia_semana == '1':
                dia = 'Domingo'
            elif horario.dia_semana == '2':
                dia = 'Segunda-feira'
            elif horario.dia_semana == '3':
                dia = 'Terça-feira'
            elif horario.dia_semana == '4':
                dia = 'Quarta-feira'
            elif horario.dia_semana == '5':
                dia = 'Quinta-feira'
            elif horario.dia_semana == '6':
                dia = 'Sexta-feira'
            else:
                dia = 'Sábado'

            temp_horario.append(dia + ' de ' + str(horario.hora_inicio)[:5] + ' às ' + str(horario.hora_fim)[:5])

        context = {
            'aluno' : aluno,
            'curso' : turma.curso,
            'data_fim' : turma.dt_fim.strftime("%d/%m/%Y"),
            'data_atual' : datetime.date.today(),
            'horarios' : temp_horario,
        }

        template_name = 'Administracao/declaracao2.html'
        return render(request, template_name,context)

    else:

        cpf = request.session["cpf"]

        if (cpf):
            try:
                aluno = Aluno.objects.get(cpf=cpf)
            except:
                print("Retorno de mais de um CPF!")
                aluno = ''
        else:
            aluno_id = request.session["aluno"]
            aluno = get_object_or_404(Aluno,id=aluno_id)

        if (aluno):

#            print ('aluno: ', aluno)

            try:
                aluno_turma = Aluno_Turma.objects.filter(aluno = aluno)
            except Exception as e:
                print (e)

            if not aluno_turma.exists():
                messages.info(request,'Aluno não consta em nenhum curso.')
                form = EscolherAlunoDeclaracao()
                return render(request,"Administracao/escolher_aluno_nova_aba.html",{'form':form})


            # desvia para tela de escolha de turma, pois um aluno pode fazer mais de um curso

            context = {
                'aluno' : aluno,
#                'aluno_turma' : aluno_turma.turma,
                'form':EscolherAlunoDeclaracao2(aluno),
            }

            return render(request, "Administracao/declaracao.html", context)


# Emitir declaração
@login_required
@permission_required('Administracao.pode_emitir_certificado', raise_exception=True)
def GerarDeclaracao2(request):

    cursando = Situacao.objects.get(descricao = "cursando")

    turma = get_object_or_404(Turma,id=aluno_turma.turma_id)
##    else:
    turma_aluno = []
#    else:
#        turma_aluno = Aluno_Turma.objects.filter(turma = turma,situacao=aprovado.id)

    temp_horario = []

    for horario in turma.horario.all():

        if horario.dia_semana == '1':
            dia = 'Domingo'
        elif horario.dia_semana == '2':
            dia = 'Segunda-feira'
        elif horario.dia_semana == '3':
            dia = 'Terça-feira'
        elif horario.dia_semana == '4':
            dia = 'Quarta-feira'
        elif horario.dia_semana == '5':
            dia = 'Quinta-feira'
        elif horario.dia_semana == '6':
            dia = 'Sexta-feira'
        else:
            dia = 'Sábado'

        temp_horario.append(dia + ' de ' + str(horario.hora_inicio)[:5] + ' a ' + str(horario.hora_fim)[:5])

    context = {
        'aluno' : aluno,
        'curso' : turma.curso,
        'data_fim' : turma.dt_fim.strftime("%d/%m/%Y"),
        'data_atual' : datetime.date.today(),
        'horarios' : temp_horario,
    }

    template_name = 'Administracao/declaracao.html'
    return render(request, template_name,context)


@login_required
@permission_required('Administracao.pode_emitir_certificado', raise_exception=True)
def lista_turmas_nao_fechadas(request):

    from datetime import date

    hoje = date.today()

    turmas = Turma.objects.filter(dt_fim__lt=hoje)
    lista = []

    for turma in turmas:
        quant = Aluno_Turma.objects.filter(turma=turma, situacao='1').count()
        if quant > 0:
            lista.append(turma)

    return render(request,"Administracao/lista_turmas_nao_fechadas.html",{'turmas':lista})



# Apresenta turmas para encerramento
@login_required
def encerrar_turma(request):
    if request.method == 'POST':
#        form = EscolherTurma(request.POST)

#        if form.is_valid():
#            turma_id = form.cleaned_data['nome']

        turma_id = request.POST.get("turma")
        turma = Turma.objects.get(pk=turma_id)

        alunos_turmas = Aluno_Turma.objects.filter(turma=turma_id).filter(situacao='1')

        if len(alunos_turmas) > 0:
            # Ainda tem aluno cursando. Nao pode encerrar turma
            msg = 'Turma não pode ser encerrada. Ainda há aluno com status CURSANDO'
        else:
            # encerra turma
            from datetime import date

            turma.dt_fechamento = date.today()
            turma.save()
            msg = 'Turma encerrada.'

        return render(request,"Administracao/turma_encerrada.html",{'turma':turma, 'msg':msg})

    usuario = User.objects.get(username=request.user.username)
    if request.user.is_superuser:
        administrador = 's'
        INSTRUTOR = ''
    else:
        administrador = 'n'
        INSTRUTOR = Instrutor.objects.get(user=usuario)

    form = EscolherTurmaEncerramento(administrador, INSTRUTOR)
    return render(request,"Administracao/escolher_turma_para_encerramento.html",{'form':form})


@login_required
def total_cadastrados_em_dado_periodo(request):
    
    if request.method == 'POST':

        form = EscolherDataCad(request.POST)
        if form.is_valid():

            dt_inicio = form.cleaned_data['dt_inicio']
            dt_fim = form.cleaned_data["dt_fim"]

        if dt_inicio == None:
            dt_inicio = '2019-01-01'

        if dt_fim == None:
            dt_fim = '2030-12-31'

        total = Aluno.objects.filter(dt_inclusao__gte=dt_inicio).filter(dt_inclusao__lte=dt_fim).count()

        return render(request, "Administracao/total_cadastrados_em_dado_periodo.html",{"dt_inicio":dt_inicio, "dt_fim":dt_fim, "total":total})

    else:
        form = EscolherDataCad()
        return render(request,"Administracao/escolher_data.html",{'form':form})

#########################

@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def cursos(request):

    cursos = Curso.objects.all()

    return render(request, "Administracao/cursos.html",{"cursos":cursos})


@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def curso_inclui(request):

    if request.method == 'POST':
        form = CursoForm(request.POST)

        if form.is_valid():
            form.save()

            form = CursoForm()

        else:
            # Se teve erro:
            print('Erro: ', form.errors)
            erro_tmp = str(form.errors)
            erro_tmp = erro_tmp.replace('<ul class="errorlist">', '')
            erro_tmp = erro_tmp.replace('</li>', '')
            erro_tmp = erro_tmp.replace('<ul>', '')
            erro_tmp = erro_tmp.replace('</ul>', '')
            erro_tmp = erro_tmp.split('<li>')

            messages.error(request, erro_tmp[2])

    else:
        form = CursoForm()

    return render(request, 'Administracao/curso_altera_inclui.html', { 'form': form, 'operacao': 'Inclusão' })


@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def curso_altera(request, id):
    curso = get_object_or_404(Curso, pk=id)

    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return render(request, 'Administracao/curso.html', { 'curso': obj })
        else:
            # Se teve erro:
            print('Erro: ', form.errors)
            erro_tmp = str(form.errors)
            erro_tmp = erro_tmp.replace('<ul class="errorlist">', '')
            erro_tmp = erro_tmp.replace('</li>', '')
            erro_tmp = erro_tmp.replace('<ul>', '')
            erro_tmp = erro_tmp.replace('</ul>', '')
            erro_tmp = erro_tmp.split('<li>')

            messages.error(request, erro_tmp[1] + ': ' + erro_tmp[2])
    else:
        form = CursoForm(instance=curso)

    return render(request, 'Administracao/curso_altera_inclui.html', { 'form': form, 'operacao': 'Alteração', 'id': curso.id })


@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def curso_exclui(request, id):
    curso = Curso.objects.get(id=id)

    return render(request, 'Administracao/curso.html', { 'curso': curso })


@login_required
@permission_required('cevest.acesso_admin', raise_exception=True)
def curso(request, id):
    curso = Curso.objects.get(id=id)

    return render(request, 'Administracao/curso.html', { 'curso': curso })


###########################
### Apagar isso após rodar

@login_required
def apaga_costurareta(request):
    curso_3 = Curso.objects.get(id=3)
    curso_21 = Curso.objects.get(id=21)

    alunos = Aluno.objects.filter(cursos=curso_3)
    for aluno in alunos:
        tem_reta = Aluno.objects.filter(id=aluno.id).filter(cursos=curso_21)
        if tem_reta:
            res = aluno.cursos.remove(curso_3)
#            res = Aluno.objects.filter(id=aluno.id).filter(cursos=curso_3).delete()
        else:
            res = aluno.cursos.add(curso_21)
            res = aluno.cursos.remove(curso_3)


