# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, QueryDict, JsonResponse
from django.forms.models import model_to_dict
from .forms import DetalheForm, CadForm, ConfirmaTurmaForm, Recibo_IndForm, Altera_cpf, CadFormBase, TesteForm
#from .forms import CadForm, ConfirmaTurmaForm, Recibo_IndForm, Altera_cpf, Altera_Cadastro, EscolherTurma#, Altera_Situacao
from .models import Curso, Aluno, Cidade, Bairro, Profissao, Escolaridade, Matriz, Turma_Prevista, Aluno_Turma, Turma, Situacao
from django.urls import reverse


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
def cursos(request):
    lista_curso = Curso.objects.filter(ativo=True, exibir=True).order_by('nome')
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

    turmas = Turma.objects.all()

    return render(request,"cevest/pauta.html",{'turmas':turmas,})

def pauta2(request, turma_id):
#    aluno = Aluno.objects.get(pk=pk)

#    alunos = Aluno.objects.select_related('Aluno_Turma',).filter(turma_id__Aluno_Turma=turma_id)

#select_related

    alunos = Aluno_Turma.objects.order_by('aluno').filter(turma=turma_id)
#    turma = Turma.objects.prefetch_related('horario__hora_inicio',).get(pk=turma_id)
    turma = Turma.objects.get(pk=turma_id)
    dias = range(20)

    return render(request,"cevest/pauta2.html",{'alunos':alunos,'dias':dias,'turma':turma,})

# ///////////////////////////////////////

# Página Cadastro
def cadastro(request):
    if request.method == 'POST':
        form = CadForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))#+form.pk)
    else:
        form = CadForm()
    return render(request,"cevest/cadastro2.html",{'form':form})#, 'cidades': cidades, 'lista_curso': lista_curso, 'escolaridades': escolaridades, 'profissoes': profissoes })
#    return render(request,"cevest/cadastro.html",{'form':form, 'cidades': cidades })

# Teste detalhe
def detalhe(request):
    if request.method == 'POST':
        form = DetalheForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            dt_nascimento = form.cleaned_data['dt_nascimento']
#            aluno = Aluno.objects.get(cpf=cpf, dt_nascimento=dt_nascimento)
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
    turmas = Turma_Prevista.objects.filter(curso=idcurso, exibir=True)
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
#    aluno = Aluno.objects.get(cpf='96847298715', dt_nascimento='2018-11-06')

    if request.method == 'POST':
        form = CadastroForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cevest/')
    else:
#        aluno = Aluno.objects.get(cpf=cpf, dt_nascimento=dt_nascimento)
        form = CadastroForm(instance=aluno)
#        form = CadastroForm(request.POST or None, instance=aluno)

    return render(request,"cevest/altera.html",{'form':form})

# /// Teste ajax

def teste_ajax(request):
    if request.method == 'POST':
        form = TesteForm(request.POST)
        print(request.POST.get('bairro'))
        if form.is_valid():
            return HttpResponseRedirect(reverse('index'))
        else:
            print("blep")
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
    #Atualiza a página em caso de dados não serem válidos ao invés de mostrar qual o erro
    if request.method == 'POST':
        altera_form = Altera_cpf(request.POST)
        if altera_form.is_valid():
            cpf_temp = altera_form.cleaned_data['cpf']
            nasc_temp = altera_form.cleaned_data['dt_nascimento']
            aluno_temp = Aluno.objects.get(cpf=cpf_temp, dt_nascimento = nasc_temp)
            request.session["aluno_id"] = aluno_temp.id
            return HttpResponseRedirect(reverse(AlterarCadastro))
    form = Altera_cpf()
    return render(request,"cevest/altera.html",{'form':form})


def AlterarCadastro(request):
    aluno_temp_id = request.session["aluno_id"]
    aluno_temp = get_object_or_404(Aluno,id=aluno_temp_id)
    if request.method == 'POST':
        form = CadFormBase(request.POST, instance = aluno_temp)
        if form.is_valid():
            form.save(aluno_temp)
            return HttpResponseRedirect(reverse('index'))
    form=CadFormBase(initial={'cidade':aluno_temp.bairro.cidade}, instance=aluno_temp)
    return render(request,"cevest/altera_cadastro.html",{'form':form})


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
