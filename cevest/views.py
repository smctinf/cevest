# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, QueryDict
from django.forms.models import model_to_dict
from .forms import CadastroForm, AlteraForm, DetalheForm, CadForm, ConfirmaTurmaForm, Recibo_IndForm, Altera_cpf
from .models import Curso, Aluno, Cidade, Bairro, Profissao, Escolaridade, Matriz, Turma_Prevista, Aluno_Turma, Turma

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
            return HttpResponseRedirect('/cevest/index')#+form.pk)
    else:
        form = CadForm()
    return render(request,"cevest/cadastro2.html",{'form':form})#, 'cidades': cidades, 'lista_curso': lista_curso, 'escolaridades': escolaridades, 'profissoes': profissoes })
#    return render(request,"cevest/cadastro.html",{'form':form, 'cidades': cidades })

def AlterarCadastro(request,aluno):
    if request.method == 'POST':
        form = CadForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cevest/index')
    else:
        form = CadForm()
    return render(request,"cevest/cadastro2.html",{'form':form})

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

import json
def get_bairro(request, cidade_id):
    if request.is_ajax():
        bairros = Bairro.objects.filter(cidade_id=cidade_id).order_by('nome')
        bairros = [ bairro_serializer(bairro) for bairro in bairros ]

        return HttpResponse(json.dumps(bairros), content_type='application/json')
    else:
        raise Http404

def bairro_serializer(bairro):
    return {'id': bairro.pk, 'nome': bairro.nome}

# /////////////////////////////////


def altera_cpf(request):
    #Pegar CPF
    #Procurar aluno com esse CPF
    #Pegar instância de aluno
    #jogar informações para CadForm
    #atualizar com .save(instance)

    if request.method == 'POST':
        cpf_temp = request.POST.get('cpf')
        aluno_temp = Aluno.objects.get(cpf=cpf_temp)
        
        #qdict = QuerryDict('')
        #qdict.update(model_to_dict(aluno_temp))
        print("what")
        #print(aluno_temp.get('nome'))
        form = CadForm(instance=aluno_temp)
        return render(request,"cevest/cadastro2.html",{'form':form})
    else:
        form = Altera_cpf()
        return render(request,"cevest/altera.html",{'form':form})

        #return render(request,"cevest/altera.html",{ 'form' : form})

def inicio(request):
    if request.user.is_authenticated:
        return render(request, 'cevest/inicio.html')
    else:
#        return render(request, 'accounts/login.html')
        return redirect('/accounts/login')

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
"""
    if request.user.is_authenticated:
        turma_prevista = Turma_Prevista.objects.all()
        if request.method == 'POST':
            form = ConfirmaTurmaForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                nome = form.cleaned_data['nome']
                curso = form.cleaned_data['curso']
                curriculo = form.cleaned_data['curriculo']
                instrutor = form.cleaned_data['instrutor']
                dt_inicio = form.cleaned_data['dt_inicio']
                dt_fim = form.cleaned_data['dt_fim']
                horario = form.cleaned_data['horario']
                quant_alunos = form.cleaned_data['quant_alunos']

                turma_prevista = form.save(commit=False)
                turma = request.user

                form.save()
            return render(request,"accounts/confirmaturma.html", {'turma_prevista':turma_prevista})
        else:
            form = ConfirmaTurmaForm()
            return render(request,"accounts/confirmaturma.html", {'turma_prevista':turma_prevista})
"""

"""
def cursos(request):
    lista_curso = Curso.objects.order_by('nome')
#    context = { 'lista_curso': lista_curso }
    return render(request, 'cevest/cursos.html', { 'lista_curso': lista_curso })
"""
"""
    if request.method == 'POST':        
        form = CadForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cevest')
#            return redirect('post_detail', pk=post.pk)
    else:
        form = CadForm()
    return render(request,"cevest/cursos.html",{'form':form})
"""


"""
def altera(request, cpf, dt_nascimento):
    aluno = Aluno.objects.get(pk=1)
#     aluno = get_object_or_404(Aluno, cpf=cpf, dt_nascimento = dt_nascimento)
    if request.method == "POST":
        form = CadForm(request.POST, instance=aluno)
        if form.is_valid():
#            aluno = form.save(commit=False)
#            aluno.author = request.user
#            aluno.published_date = timezone.now()
            form.save()
            return HttpResponseRedirect('/cevest')
#            return redirect('post_detail', pk=aluno.pk)
    else:
        form = CadForm(instance=aluno)
    return render(request, 'cevest/cad.html', {'form': form})
"""
"""
def altera(request):
    if request.method == 'POST':        
        form = CadForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cevest')
#            return redirect('post_detail', pk=post.pk)
    else:
        form = CadForm()
    return render(request,"cevest/altera.html",{'form':form})
"""
"""
def cadastro(request):
    lista_curso = Curso.objects.order_by('-nome')[:5]
#    template = loader.get_template('cevest/cadastro.html')
    context = {
        'lista_curso': lista_curso,
    }
    if request.method == 'POST':
        context = {
            'lista_curso': lista_curso, 'teste' : request.POST
        }
        
        form = CadastroForm(request.POST)
 
        if form.is_valid():
#            Aluno_Quer_Curso.curso(1)
            Aluno_Quer_Curso.save()
            form.save()
#            chave = CadastroForm.pk
#            return redirect('')
    else:
#        context = { 'lista_curso': lista_curso }
        form = CadastroForm()
 
#    return render(request,"cevest/cadastro.html",{'form':form, 'lista_curso': lista_curso})
    return render(request,"cevest/cadastro.html",{'form':form})

#    lista_curso = Curso.objects.order_by('-nome')[:5]
#    context = { 'lista_curso': lista_curso }
#    return render(request, 'cevest/cadastro.html', context)

# def cadastro_new(request):
#     form = CadastroForm()
#     return render(request, 'cevest/cadastro_edit.html', {'form': form})
"""

"""
# Exemplo teste
def teste(request):
    latest_question_list = Curso.objects.order_by('-nome')[:5]
    output = '<br>'.join([q.nome for q in latest_question_list])
    return HttpResponse(output)
"""
