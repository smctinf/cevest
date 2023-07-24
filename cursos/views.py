from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404

from autenticacao.functions import aluno_required
from .models import *
from .forms import *
from datetime import date, datetime

from .models import *
from .forms import *
from autenticacao.forms import Form_Pessoa
from eventos.models import Evento
from django.apps import apps
from random import shuffle

from django.urls import reverse
def index(request):
    try:
        eventos = Evento.objects.filter(app_name='cursos', is_destaque = True)
    except:
        eventos=[]
    
    cursos = list(Curso.objects.filter(tipo='C', ativo=True).order_by('?')[:4])
    palestras = list(Curso.objects.filter(tipo='P', ativo=True).order_by('?')[:4])
    shuffle(cursos)
    context = { 
        'titulo': apps.get_app_config('cursos').verbose_name,
        'eventos': eventos,
        'cursos': cursos,   
        'cursos_en': Curso_Ensino_Superior.objects.all()[:4],
        'palestras': palestras 
    }

    return render(request, 'cursos/index.html', context)



def cursos(request, tipo):
    form = Aluno_form()
    categorias = Categoria.objects.all()
    cursos = []
    if tipo == 'cursos':        
            cursos=Curso.objects.filter(tipo='C', ativo=True)
    elif tipo == 'palestras':
            cursos=Curso.objects.filter(tipo='P', ativo=True)    

    context = {
        'categorias':categorias,
        'cursos': cursos,
        'form': form,
        'titulo': apps.get_app_config('cursos').verbose_name,        
        'tipo': tipo
    }
    if tipo == 'cursos':
        return render(request, 'cursos/cursos.html', context)
    elif tipo == 'palestras':  
        return render(request, 'cursos/palestras.html', context)
    raise Http404("Página não encontrada")  

def cursos_filtrado(request, tipo, filtro):
    form = Aluno_form()
    categorias = Categoria.objects.all()
    cursos = []
    if tipo == 'cursos':       
       cursos=Curso.objects.filter(tipo='C', categoria__nome=filtro, ativo=True)
    elif tipo == 'palestras':                
        cursos=Curso.objects.filter(tipo='P', categoria__nome=filtro, ativo=True)

    context = {
        'categorias': categorias,
        'cursos': cursos,
        'form': form,
        'titulo': apps.get_app_config('cursos').verbose_name,
        'filtro': filtro,
        'tipo': tipo
    }
    if tipo == 'cursos':
        return render(request, 'cursos/cursos.html', context)
    elif tipo == 'palestras':  
        return render(request, 'cursos/palestras.html', context)
    raise Http404("Página não encontrada")

def curso_detalhe(request, tipo, id):    
    curso=Curso.objects.get(id=id)    
    context={
        'curso': curso,
        'tipo': tipo,
        'titulo': apps.get_app_config('cursos').verbose_name,
        'turmas': Turma.objects.filter(curso=curso)
    }
    return render(request, 'cursos/curso_detalhe.html', context)

@login_required
def candidatar(request, id):

    curso = Curso.objects.get(id=id)
    form = Aluno_form(initial={'curso': curso})
    if request.method == 'POST':
        form = Aluno_form(request.POST)
        if form.is_valid():
            form.save()

    context = {
        'form': form,
        'titulo': apps.get_app_config('cursos').verbose_name,
    }
    return render(request, 'cursos/cadastrar_candidato.html', context)


def prematricula(request):
    form = Aluno_form(prefix="candidato")
    form_responsavel = CadastroResponsavelForm(prefix="responsavel")

    categorias = Categoria.objects.all()
    cursos = []

    for i in categorias:
        cursos.append(
            {'categoria': i, 'curso': Curso.objects.filter(categoria=i, ativo=True)})

    if request.method == 'POST':
        dtnascimento_cp = request.POST.get("candidato-dt_nascimento")
        form = Aluno_form(request.POST, prefix="candidato")
        form_responsavel = CadastroResponsavelForm(
            request.POST, prefix="responsavel")

        try:
            dtnascimento_hr = datetime.strptime(dtnascimento_cp, "%d-%m-%Y")
        except:
            dtnascimento_hr = datetime.strptime(dtnascimento_cp, "%Y-%m-%d")

        dt_nascimento = dtnascimento_hr.date()

        today = date.today()
        age = today.year - dt_nascimento.year - \
            ((today.month, today.day) < (dt_nascimento.month, dt_nascimento.day))
        teste = True
        candidato = False

        try:
            cpf = request.POST['cpf']
            candidato = Aluno.objects.get(cpf=cpf)
        except Exception as e:
            pass

        if candidato:        
            turma = Turma.objects.get(id=i)
            if candidato:
                try:
                    Matricula.objects.get(
                        candidato=candidato, turma__curso=turma.curso)
                    messages.error(
                        request, 'Candidato já matriculado no curso ' + turma.curso.nome)
                    return redirect('cursos:curso_detalhe')
                except:
                    pass

            if (turma.idade_minima is not None and age < turma.idade_minima) or (turma.idade_maxima is not None and age > turma.idade_maxima):
                teste = False

        if form.is_valid() and teste:
            candidato = form.save(commit=False)

            if age < 18:

                if form_responsavel.is_valid():

                    responsavel = form_responsavel.save(commit=False)
                    responsavel.aluno = candidato

                else:
                    return redirect('cursos:curso_detalhe')

                responsavel.save()
                candidato.save()

            else:

                candidato.save()

            for i in request.POST.getlist('turmas'):
                Matricula.objects.create(
                    aluno=candidato, turma=turma, status='c')

            messages.success(
                request, 'Pré-inscrição realizada com sucesso! Aguarde nosso contato para finalizar inscrição.')
            return redirect('/')
        else:
            if not teste:
                messages.error(
                    request, 'Não foi possível realizar a inscrição na turma: A idade não atende a faixa etária da turma.')
                return redirect('/prematricula')

    context = {
        'form': form,
        'form_responsavel': form_responsavel,
        'categorias': cursos,
        'titulo': 'Capacitação Profissional'
    }
    return render(request, 'cursos/pre_matricula.html', context)


def login_view(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if "next" in request.GET:
                return redirect(request.GET.get('next'))
            return redirect('/')
        else:
            context = {
                'error': True,
            }

    return render(request, 'registration/login.html', context)


def alterarCad(request):
    return render(request, 'cursos/alterar_cad.html')


def resultado(request):
    return render(request, 'cursos/resultado.html')

@login_required
def matricular(request, tipo, id):
    curso=Curso.objects.get(id=id)
    pessoa=Pessoa.objects.get(user=request.user)

    #checa se já é aluno para por informações no formulario
    try:
        aluno=Aluno.objects.get(pessoa=pessoa)
        form = Aluno_form(prefix="candidato", instance=aluno)
        try:            
            form_responsavel = CadastroResponsavelForm(prefix="responsavel", instance=aluno)
        except:
            pass
    except Exception as E:        
        aluno=None     
        form = Aluno_form(prefix="candidato")    
        form_responsavel = CadastroResponsavelForm(prefix="responsavel")

    # Checa a idade e se precisa de responsavel
    dtnascimento = pessoa.dt_nascimento    
    today = date.today()
    age = today.year - dtnascimento.year - \
            ((today.month, today.day) < (dtnascimento.month, dtnascimento.day))    
    precisa_responsavel=age<18
    
    if request.method == 'POST':
        
        form = Aluno_form(request.POST, prefix="candidato", instance=aluno)
        if precisa_responsavel:
            form_responsavel = CadastroResponsavelForm(
                request.POST, prefix="responsavel", instance=aluno)

        
        teste = True        
        
        candidato = aluno
        

        #checando idade minima e maxima para o curso
        turmas=Turma.objects.filter(curso=curso)
        pode_cursar=True
        if len(turmas)!=0:
            for turma in turmas:
                if (turma.idade_minima is not None and age < turma.idade_minima) or (turma.idade_maxima is not None and age > turma.idade_maxima):
                    teste = False
                    if not teste:
                        print('entrou aqui')
                        pode_cursar=False
                        teste=True
            
        #validação das informações do forms
        if form.is_valid() and pode_cursar:
            if candidato:
                for turma in turmas:
                    try:
                        Matricula.objects.get(
                            aluno=candidato, turma__curso=turma.curso)
                        messages.error(
                            request, 'Candidato já matriculado no curso: ' + turma.curso.nome)
                        return redirect(reverse('cursos:curso_detalhe', args=[tipo, id]))
                    except Exception as E:                        
                        pass
            candidato = form.save(commit=False)

            if precisa_responsavel:
                if form_responsavel.is_valid():
                    responsavel = form_responsavel.save(commit=False)
                    responsavel.aluno = candidato
                else:       
                    messages.warning(
                    request, 'Preencha corretamente os campos do formulário!')
                    context = {
                        'age': age,
                        'form': form,
                        'form_responsavel': form_responsavel,     
                        'titulo': 'Capacitação Profissional',
                        'curso': curso,
                        'pessoa': pessoa
                    }             
                    return render(request, 'cursos/pre_matricula.html', context)
                candidato.pessoa=pessoa
                candidato.save()                                
                responsavel.save()
                
            else:
                candidato.pessoa=pessoa
                candidato.save()                    
                print(candidato.pessoa.nome)

            #criando matricula como candidato na turma
            try:
                turma=Turma.objects.get(curso=curso, status='pre')
                Matricula.objects.create(
                    aluno=candidato, turma=turma, status='c')
            except:     
                try:
                    turma=Turma.objects.get(curso=curso, status='acc')
                    Matricula.objects.create(
                        aluno=candidato, turma=turma, status='c')
                except:
                    Alertar_Aluno_Sobre_Nova_Turma.objects.create(
                        aluno=candidato,
                        curso=curso
                    )
                    messages.success(
                    request, 'Você será informado quando abrir o a inscrição de uma nova turma para este curso!')
                    return redirect(reverse('cursos:matricula', args=[tipo,id]))
            

            messages.success(
                request, 'Pré-inscrição realizada com sucesso! Aguarde nosso contato para finalizar inscrição.')
            print('passou aqui 2')
            return redirect(reverse('cursos:curso_detalhe', args=[tipo, id]))
        else:
            print('passou aqui')
            if not teste:
                messages.error(
                    request, 'Não foi possível realizar a inscrição na turma: A idade não atende a faixa etária da turma.')
                return redirect(reverse('cursos:curso_detalhe', args=[tipo, id]))

    context = {
        'age': age,
        'form': form,
        'form_responsavel': form_responsavel,     
        'titulo': 'Capacitação Profissional',
        'curso': curso,
        'pessoa': pessoa
    }
    return render(request, 'cursos/pre_matricula.html', context)

def ensino_superior(request):
    context = {
        'titulo': 'Capacitação Profissional',
        'cursos': Curso_Ensino_Superior.objects.all()
    }
    return render(request, 'cursos/ensino_superior.html', context)

# def ensino_superior_detalhe(request, id):    
#     curso=Curso.objects.get(id=id)
#     context={
#         'curso': curso,
#         'tipo': tipo,
#         'titulo': apps.get_app_config('cursos').verbose_name,
#         'turmas': Turma.objects.filter(curso=curso)
#     }
#     return render(request, 'cursos/curso_detalhe.html', context)

def ensino_tecnico(request):
    context = {
        'titulo': 'Capacitação Profissional',
        # 'cursos': Curso_Ensino_Superior.objects.all()
    }
    return render(request, 'cursos/ensino_tecnico.html', context)

def curriculo_vitae(request):
    context = {
        'titulo': 'Capacitação Profissional'
    }
    return render(request, 'cursos/curriculo_vitae.html', context)

def area_do_estudante(request):
    pessoa=Pessoa.objects.get(user=request.user)
    aluno=Aluno.objects.get(pessoa=pessoa)
    matriculas=Matricula.objects.filter(aluno=aluno)
    alertas=Alertar_Aluno_Sobre_Nova_Turma.objects.filter(aluno=aluno)
    context={
        'matriculas': matriculas,
        'alertas': alertas,
    }
    return render(request, 'cursos/area_do_estudante.html', context)

def editar_cadastro(request):    
    pessoa=Pessoa.objects.get(user=request.user)
    form_pessoa=Form_Pessoa(instance=pessoa)    
    if request.method == 'POST':
        form_pessoa=Form_Pessoa(request.POST, instance=pessoa)
        if form_pessoa.is_valid:
            form_pessoa.save()
    context={        
        'form_pessoa': form_pessoa
    }
    return render(request, 'cursos/editar_cadastro.html', context)