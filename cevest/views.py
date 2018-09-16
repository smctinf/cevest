# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .forms import CadastroForm

def index(request):
#    lista_curso = Curso.objects.order_by('-nome')[:5]
#    context = { 'lista_curso': lista_curso }
    return render(request, 'cevest/index.html')

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
 
        if form.is_valid():
            form.save()
#            return redirect('')
    else:
        form = CadastroForm()
 
    return render(request,"cevest/cadastro.html",{'form':form})

#    lista_curso = Curso.objects.order_by('-nome')[:5]
#    context = { 'lista_curso': lista_curso }
#    return render(request, 'cevest/cadastro.html', context)

# def cadastro_new(request):
#     form = CadastroForm()
#     return render(request, 'cevest/cadastro_edit.html', {'form': form})