# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import CadastroForm, CadForm
from .models import Curso, Aluno

def teste(request):
    latest_question_list = Curso.objects.order_by('-nome')[:5]
    output = '<br>'.join([q.nome for q in latest_question_list])
    return HttpResponse(output)

def index(request):
#    lista_curso = Curso.objects.order_by('-nome')[:5]
#    context = { 'lista_curso': lista_curso }
    return render(request, 'cevest/index.html')

def cursos(request):
    lista_curso = Curso.objects.order_by('nome')
#    context = { 'lista_curso': lista_curso }
    return render(request, 'cevest/cursos.html', { 'lista_curso': lista_curso })

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

def cad(request):
    if request.method == 'POST':        
        form = CadForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cevest')
#            return redirect('post_detail', pk=post.pk)
    else:
        form = CadForm()
    return render(request,"cevest/cad.html",{'form':form})

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