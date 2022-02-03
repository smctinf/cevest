# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, QueryDict, JsonResponse
from django.forms.models import model_to_dict
from .forms import *
from .models import *
from django.urls import reverse
from django.contrib import messages
import datetime
from django.db.models import Count, Q, Sum, Avg

# Página index
def aguarde(request):
    return render(request, 'cevest/aguarde.html')

# Página index
def index(request):
    return render(request, 'cevest/index.html')

# Página Resultado
def resultado(request):
    return render(request, 'cevest/resultado.html')

# Página Cursos
def cursos(request, pk):
    lista_curso = Curso.objects.filter(ativo=True, exibir=True, programa=pk).order_by('nome')
    return render(request, 'cevest/cursos.html', { 'lista_curso': lista_curso })

# Página Detalhes de um Curso
def curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)

    return render(request,"cevest/curso.html", {'curso':curso})

def recibo_ind(request):
    if request.method == 'POST':
        form = Recibo_IndForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo']
            return HttpResponseRedirect('/recibo_ind/'+codigo)
    else:
        form = Recibo_IndForm()
        return render(request,"cevest/altera.html",{'form':form,})

def recibo_ind2(request, pk):
#    aluno = Aluno.objects.get(pk=pk)
    aluno = Aluno.objects.get(cpf='05334010700', dt_nascimento='1978-11-02')

    return render(request,"cevest/recibo_ind.html",{'aluno':aluno,})

#//////////////////
#// Imprime pauta
#//////////////////

def pauta(request):

    if request.user.is_superuser or request.user.has_perm('Administracao.pode_emitir_certificado'):
        turmas = Turma.objects.filter(dt_fechamento=None)
    else:
        user = User.objects.get(username=request.user.username)
        instrutor = Instrutor.objects.get(user=user)
        turmas = Turma.objects.filter(instrutor=instrutor).filter(dt_fechamento=None)

    return render(request,"cevest/pauta.html",{'turmas':turmas,})

def pauta2(request, turma_id):
#    aluno = Aluno.objects.get(pk=pk)

#    alunos = Aluno.objects.select_related('Aluno_Turma',).filter(turma_id__Aluno_Turma=turma_id)

#select_related

    alunos = Aluno_Turma.objects.order_by('aluno').filter(turma=turma_id).filter(situacao=1)
#    turma = Turma.objects.prefetch_related('horario__hora_inicio',).get(pk=turma_id)
    turma = Turma.objects.get(pk=turma_id)
    dias = range(20)

    return render(request,"cevest/pauta2.html",{'alunos':alunos,'dias':dias,'turma':turma,})

# ///////////////////////////////////////

# Página Cadastro
def cadastro(request):

    programas = Programa.objects.filter(ativo=True).order_by('-nome')

    cursos = []

    for programa in programas:
        cursos_pgm = Curso.objects.filter(programa=programa).filter(exibir=True).filter(ativo=True)
        cursos.append({'programa': programa, 'cursos': cursos_pgm})

    if request.method == 'POST':
        form = CadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,'Cadastro Salvo')
            return HttpResponseRedirect(reverse('index'))

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
        form = CadForm()
    return render(request,"cevest/cadastro2.html",{'form':form, 'cursos':cursos})

# Teste detalhe
def detalhe(request):
    if request.method == 'POST':
        form = DetalheForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            dt_nascimento = form.cleaned_data['dt_nascimento']
            aluno = Aluno.objects.get(cpf='05334010700', dt_nascimento='1978-11-02')
            if aluno != 'None':
                pk = aluno.pk
#                form = AlteraForm()
#                return render(request,"cevest/altera.html", aluno)
            return redirect ('altera/'+str(pk))
#            else:
#            return render(request, 'cevest/detalhe.html')
#        print('teste')
    else:
        return render(request, 'cevest/detalhe.html')

# Página Matriz Curricular de um Curso
def matriz(request, idcurso):
    disciplinas = Matriz.objects.filter(curso=idcurso)
    curso = Curso.objects.get(pk=idcurso)

    return render(request,"cevest/matriz.html", {'disciplinas':disciplinas, 'curso': curso})

# Página Turma Prevista de um Curso
def turma_prevista(request, idcurso):
    turmas = Turma.objects.filter(curso=idcurso, exibir=True, dt_fim__gt = datetime.date.today())
    curso = Curso.objects.get(pk=idcurso)

    return render(request,"cevest/turma_prevista.html", {'turmas':turmas, 'curso': curso})

# Página Turma Prevista de um Curso
def portador(request):
    if request.user.is_authenticated:
        portador = Aluno.objects.filter(portador_necessidades_especiais=True).order_by('nome')
#        alocados = Aluno_Turma_Prevista.objects.filter(portador_necessidades_especiais=True).order_by('nome')
        return render(request,"cevest/portador.html", {'portador':portador})
    else:
        return HttpResponseRedirect('/accounts/login')

def altera(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        form = CadastroForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cevest/')

    else:
        form = CadastroForm(instance=aluno)

    return render(request,"cevest/altera.html",{'form':form})

# /// Teste ajax

def teste_ajax(request):
    if request.method == 'POST':
        form = TesteForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('index'))
        else:
            print("erro form ajax")
    else:
        form = TesteForm()
    return render(request,"cevest/teste.html",{'form':form})

def load_bairros(request):
    cidade_id = request.GET.get('id')
    bairros = Bairro.objects.filter(cidade = cidade_id).order_by('nome')
    return render(request, 'cevest/teste_options.html', {'bairros' : bairros})

import json
def get_bairro(request, cidade_id):
    if request.is_ajax():
        bairros = Bairro.objects.filter(cidade_id=cidade_id).order_by('nome')
        bairros = [ bairro_serializer(bairro) for bairro in bairros ]

        return HttpResponse(json.dumps(bairros), content_type='application/json')
    else:
        raise Http404

def bairro_serializer(bairro):
    return {'id': bairro.id, 'nome': bairro.nome}

# /////////////////////////////////

def altera_cpf(request):

    if request.method == 'POST':

        altera_form = Altera_cpf(request.POST)

        if altera_form.is_valid():

            cpf_temp = altera_form.cleaned_data['cpf']
            nasc_temp = altera_form.cleaned_data['dt_nascimento']

            try:
                aluno_temp = Aluno.objects.get(cpf=cpf_temp, dt_nascimento = nasc_temp)
            except Aluno.DoesNotExist:
                aluno_temp = None
                messages.info(request,'Cadastro inexistente')

                form = altera_form
                return render(request,"cevest/altera.html",{'form':form})

            request.session["aluno_id"] = aluno_temp.id
            return HttpResponseRedirect(reverse(AlterarCadastro))
        else:
            # Se teve erro:
            print('Erro: ', altera_form.errors)
            erro_tmp = str(altera_form.errors)
            erro_tmp = erro_tmp.replace('<ul class="errorlist">', '')
            erro_tmp = erro_tmp.replace('</li>', '')
            erro_tmp = erro_tmp.replace('<ul>', '')
            erro_tmp = erro_tmp.replace('</ul>', '')
            erro_tmp = erro_tmp.split('<li>')

            messages.error(request, erro_tmp[2])

            form = altera_form
    else:
        form = Altera_cpf()

    return render(request,"cevest/altera.html",{'form':form})


def AlterarCadastro(request):
    aluno_temp_id = request.session["aluno_id"]
    aluno_temp = get_object_or_404(Aluno,id=aluno_temp_id)
    checked_curso_ids = []
    for curso in aluno_temp.cursos.all():
        checked_curso_ids.append(curso.id)
    if request.method == 'POST':
        form = CadFormBase(request.POST, instance = aluno_temp)
        if form.is_valid():
            form.save(aluno_temp)
            messages.info(request,'Cadastro Salvo')
            return HttpResponseRedirect(reverse('index'))

        else:
            print('Erro: ', form.errors)
            erro_tmp = str(form.errors)
            erro_tmp = erro_tmp.replace('<ul class="errorlist">', '')
            erro_tmp = erro_tmp.replace('</li>', '')
            erro_tmp = erro_tmp.replace('<ul>', '')
            erro_tmp = erro_tmp.replace('</ul>', '')

            erro_tmp = erro_tmp.split('<li>')

            messages.error(request, erro_tmp[1] + ': ' + erro_tmp[2])


    # Carrega cursos separado por programas
    programas = Programa.objects.all().order_by('-nome')

    cursos = []

    for programa in programas:
        cursos_pgm = Curso.objects.filter(programa=programa).filter(exibir=True).filter(ativo=True)
        cursos.append({'programa': programa, 'cursos': cursos_pgm})


    # 
    form=CadFormBase(initial={'cidade':aluno_temp.bairro.cidade}, instance=aluno_temp)
    return render(request,"cevest/altera_cadastro.html",{'form':form, 'cursos':cursos, 'checked_curso_ids':checked_curso_ids})


#???
def inicio(request):
    if request.user.is_authenticated:
        return render(request, 'cevest/inicio.html')
    else:
#        return render(request, 'accounts/login.html')
        return redirect('/accounts/login')

#???
def sair(request):
    if request.user.is_authenticated:
        return redirect('/accounts/logout')
    else:
        return redirect('/accounts/login')

def alocados(request):
    if request.user.is_authenticated:
        cursos = Curso.objects.filter(ativo=True)[1]
        quant_necessidades_especiais = int(cursos.quant_alunos * 0.3)
        necessidades = Aluno_Turma.objects.raw('select cevest_aluno.id as aluno_id, cevest_turma_prevista.id as turma_id from cevest_aluno, cevest_turma_prevista, cevest_aluno_cursos where cevest_aluno, cevest_turma_prevista.id and cevest_aluno_cursos.curso_id = cursos.id and cevest_aluno.cursos_id = cursos.id')
#        necessidades = Aluno.objects.filter(portador_necessidades_especiais=True, curso_id=cursos.id)[quant_necessidades_especiais]
        return HttpResponse("Cursos %s." % necessidades)

    else:
        return redirect('/accounts/login')

def confirmaturma(request):
    form = ConfirmaTurmaForm()
    return render(request, "accounts/confirmaturma.html", {'form': form})

def getLista_Candidatos():
    situacao_cancelada = Situacao_Turma.objects.get(descricao = "Cancelada")
    turmas_previstas_remover = Turma_Prevista.objects.filter(situacao = situacao_cancelada)
    turmas_previstas_remover = turmas_previstas_remover.filter(dt_fim__lt = datetime.date.today())

    status = Status_Aluno_Turma_Prevista.objects.get(descricao = "Candidato")

    aluno_turma = Aluno_Turma_Prevista.objects.filter(status_aluno_turma_prevista = status).order_by("aluno")

    for turma in turmas_previstas_remover:
        aluno_turma = aluno_turma.exclude(turma_prevista = turma)


    return aluno_turma


def getLista_Alocados():
    situacao_cancelada = Situacao_Turma.objects.get(descricao = "Cancelada")
    turmas_previstas = Turma_Prevista.objects.exclude(situacao = situacao_cancelada)
    turmas_previstas = turmas_previstas.exclude(dt_fim__lt = datetime.date.today())

    lista_turmas = []

    for turma in turmas_previstas:
        temp_lista_alunos = []
        temp_lista_horarios = []
        temp_turma_aluno = Aluno_Turma_Prevista.objects.filter(turma_prevista = turma)
        for aluno_turma in temp_turma_aluno:
            temp_lista_alunos.append(aluno_turma.aluno)
        print ('hora:')
        for horario in turma.horario.all():
            print (horario)
            temp_lista_horarios.append(horario)
        print (temp_lista_horarios)
        lista_turmas.append({"turma":turma,"alunos":temp_lista_alunos,"horarios":temp_lista_horarios})
    return lista_turmas

    

def lista_alocados(request):
    lista_turmas = getLista_Alocados()
    return render(request, "cevest/lista_alocados.html",{"listas":lista_turmas})

def getLista_TurmaConfirmada():
    turmas = Turma.objects.exclude(dt_fim__lt = datetime.date.today())

    lista_turmas = []

    for turma in turmas:
        temp_lista_alunos = []
        temp_lista_horarios = []
        temp_turma_aluno = Aluno_Turma.objects.filter(turma = turma)
        for aluno_turma in temp_turma_aluno:
            temp_lista_alunos.append(aluno_turma.aluno)
        for horario in turma.horario.all():
            temp_lista_horarios.append(horario)
        if len(temp_lista_alunos) > 0:
            lista_turmas.append({"turma":turma,"alunos":temp_lista_alunos,"horarios":temp_lista_horarios})
    return lista_turmas

def lista_turma(request):
    lista_turmas = getLista_TurmaConfirmada()
    return render(request, "cevest/lista_alocados.html",{"listas":lista_turmas})

def getLista_NaoAlocados():
    temp_lista = Aluno.objects.all()

    lista_alocados = Aluno_Turma_Prevista.objects.all()
    lista_ids = []
    for aluno_turma in lista_alocados:
        lista_ids.append(aluno_turma.aluno.id)

    temp_lista = temp_lista.exclude(id__in = lista_ids)
    return temp_lista

def getTotalPorSexo():
    feminino = Aluno.objects.filter(sexo = 'F').count()
    masculino = Aluno.objects.filter(sexo = 'M').count()
    lista = []
    lista_temp = []
    lista_temp.append("F")
    lista_temp.append(feminino)
    lista.append(lista_temp)
    lista_temp = []
    lista_temp.append("M")
    lista_temp.append(masculino)
    lista.append(lista_temp)
    lista = sorted(lista, key = lambda i: (-i[1]))
    #returna um dicionário com lista sendo uma lista de listas(matriz) com as linhas/colunas da tabela, o título e uma lista de strings para serem os headers da tabela
    return {'lista':lista, 'titulo': 'Total Por Sexo', 'table_headers':['Sexo','Total']}

def getTotalPorCurso():
    lista = []
    cursos = Curso.objects.all()
    lista_temp_cursos = []
    cursos = cursos.annotate(curso_count = Count('aluno'))

    for curso in cursos:
        lista_temp = []
        lista_temp.append(curso.nome)
        lista_temp.append(curso.curso_count)
        lista.append(lista_temp)


    lista = sorted(lista, key = lambda i: (-i[1]))
    #returna um dicionário com lista sendo uma lista de listas(matriz) com as linhas/colunas da tabela, o título e uma lista de strings para serem os headers da tabela
    return {'lista':lista, 'titulo': 'Total Interesse Por Curso', 'table_headers':['Curso','Total']}

def getTotalMatriculadoPorTurma():
    lista = []
    turmas = Turma.objects.all()
    turmas = turmas.annotate(turma_count = Count('aluno_turma'))
    for turma in turmas:
        temp_lista = []
        temp_lista.append(turma.curso)
        temp_lista.append(turma.nome)
        temp_lista.append(turma.turma_count)
        temp_lista.append(turma.quant_alunos)
        lista.append(temp_lista)

    lista = sorted(lista, key = lambda i: (-i[2]))
    #returna um dicionário com lista sendo uma lista de listas(matriz) com as linhas/colunas da tabela, o título e uma lista de strings para serem os headers da tabela
    return {'lista': lista, 'titulo': 'Total Matriculado Por Turma', 'table_headers':['Curso','Turma','Total Alunos','Vagas'] }

def getTotalPorBairro():
    lista = []
    bairros = Bairro.objects.all()
    for bairro in bairros:
        temp_lista = []
        temp_lista.append(bairro.nome)
        temp_lista.append(Aluno.objects.filter(bairro=bairro).count())
        #print(temp_lista[1].query)
        lista.append(temp_lista)

    lista = sorted(lista, key = lambda i: (-i[1]))

    #returna um dicionário com lista sendo uma lista de listas(matriz) com as linhas/colunas da tabela, o título e uma lista de strings para serem os headers da tabela
    return {'lista': lista, 'titulo': 'Total Por Bairro', 'table_headers':['Bairro','Total'] }

def getTotalPorProfissao():
    lista = []
    profissoes = Profissao.objects.all()
    profissoes = profissoes.annotate(count = Count('aluno'))
    for profissao in profissoes:
        temp_lista = []
        temp_lista.append(profissao.nome)
        temp_lista.append(profissao.count)
        lista.append(temp_lista)

    lista = sorted(lista, key = lambda i: (-i[1]))

    #returna um dicionário com lista sendo uma lista de listas(matriz) com as linhas/colunas da tabela, o título e uma lista de strings para serem os headers da tabela
    return {'lista': lista, 'titulo': 'Total Por Profissão', 'table_headers':['Profissão','Total'] }

def getTotalConcluidosPorCurso():
    lista = []

    situacao_aprovado = Situacao.objects.get(descricao = "Aprovado")
    cursos = Curso.objects.all()

    temp_total_geral = 0

    for curso in cursos:    
        turmas = Turma.objects.filter(curso = curso)
        lista_temp = []
        temp_total = 0
        for turma in turmas:
            temp_total += Aluno_Turma.objects.filter(turma = turma, situacao = situacao_aprovado).count()
        #ignorar as três linhas seguintes se não tiver concluidos?
        lista_temp.append(curso.nome)
        lista_temp.append(temp_total)
        lista.append(lista_temp)
        temp_total_geral += temp_total

    lista = sorted(lista, key = lambda i: (-i[1]))

    #mostra total geral (depois do sort para o total ficar no final)
    lista.append(['Total Geral', temp_total_geral])

    #returna um dicionário com lista sendo uma lista de listas(matriz) com as linhas/colunas da tabela, o título e uma lista de strings para serem os headers da tabela
    return {'lista': lista, 'titulo': 'Concluídos por turma', 'table_headers':['Turma','Total'] }

def getInteresseTotalPorCursoETurno():
    lista = []
    cursos = Curso.objects.all()
    lista_temp_cursos = []

    manha = Turno.objects.get(descricao = "Manhã")
    tarde = Turno.objects.get(descricao = "Tarde")
    noite = Turno.objects.get(descricao = "Noite")

    for curso in cursos:
        lista_temp_cursos.append({'Curso':curso, manha:0, tarde:0, noite:0})


    alunos = Aluno.objects.all()

    #print(cursos.annotate(curso_count = Count('aluno'))[0].curso_count)

    #Trocar esses fors por queries pra ver se demora menos de 20 milhões de anos para a página carregar
    for aluno in alunos:
        for curso in aluno.cursos.all():
            for curso_temp in lista_temp_cursos:
                if curso_temp['Curso'] == curso:
                    for turno in aluno.disponibilidade.all():
                        curso_temp[turno] += 1

    for temp in lista_temp_cursos:
        lista_temp = []
        lista_temp.append(temp['Curso'].nome)
        lista_temp.append(temp[manha])
        lista_temp.append(temp[tarde])
        lista_temp.append(temp[noite])
        lista.append(lista_temp)


    lista = sorted(lista, key = lambda i: (-(i[1]+i[2]+i[3])))

    #returna um dicionário com lista sendo uma lista de listas(matriz) com as linhas/colunas da tabela, o título e uma lista de strings para serem os headers da tabela
    return {'lista':lista, 'titulo': 'Total Interesse Por Curso', 'table_headers':['Curso','Manhã','Tarde','Noite']}

def indicadores(request):
    #Precisa de uma lista com um dicionário com lista sendo uma lista de listas(matriz) com as linhas/colunas da tabela, o título e uma lista de strings para serem os headers da tabela
    #Nessas condições o html renderiza qualquer combinação de tabelas

    indicadores_lista = []
    indicadores_lista.append(getTotalPorSexo())
    indicadores_lista.append(getTotalPorCurso())
    indicadores_lista.append(getTotalMatriculadoPorTurma())
    indicadores_lista.append(getTotalPorBairro())
    indicadores_lista.append(getTotalPorProfissao())
    indicadores_lista.append(getTotalConcluidosPorCurso())
    #Retirar/comentar a linha seguinte se demorar muito pra carregar(até mudar os fors dentro da função getInteresseTotalPorCursoETurno para queries)
    #indicadores_lista.append(getInteresseTotalPorCursoETurno())
    return render(request, "cevest/indicadores.html",{"indicadores":indicadores_lista})
