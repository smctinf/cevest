import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator
from django.apps import apps
from django.db.models import Count

from .models import *
from .forms import *

def index(request):
    data = Material.objects.all()
    paginator = Paginator(data, 30)
    page = request.GET.get('page', 1)
    materiais = paginator.get_page(page)

    context = {
        'titulo': apps.get_app_config('cevest_almoxarifado').verbose_name,
        'materiais': materiais
    }
    return render(request, 'cevest_almoxarifado/index.html', context)


def listar_tipo_materiais(request):
    context = {
        'titulo': apps.get_app_config('cevest_almoxarifado').verbose_name,
        'tipos': Tipo_Material.objects.all()
    }
    return render(request, 'cevest_almoxarifado/listar_tipo_materiais.html', context)


def adicionar_tipo_materiais(request):
    if request.method == 'POST':
        form = Tipo_Material_Form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de material cadastrado!')
            return redirect('cevest_almoxarifado:index')
    else:
        form = Tipo_Material_Form()

    context = {
        'titulo': apps.get_app_config('cevest_almoxarifado').verbose_name,
        'form': form
    }
    return render(request, 'cevest_almoxarifado/adicionar_tipo_materiais.html', context)

def adicionar_material(request, tipo):
    tipo = Tipo_Material.objects.get(id=tipo)

    if request.method == 'POST':
        form = Material_Form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material cadastrado!')
            return redirect('cevest_almoxarifado:alm_listar_tipos')
    else:
        form = Material_Form(initial={'tipo': tipo.id})

    context = {
        'titulo': apps.get_app_config('cevest_almoxarifado').verbose_name,
        'form': form
    }
    return render(request, 'cevest_almoxarifado/adicionar_novo_material.html', context)

@login_required
def getMaterial(request, id):
    opcoes = Material.objects.filter(tipo=id).values('id', 'nome')
    return JsonResponse(list(opcoes), safe=False)

@login_required
def adicionar_material_ao_estoque(request):
    if request.method == 'POST':
        form = Log_estoque_Form(request.POST)
        form_tipo = Exibir_Tipo_Material_Form(request.POST)
        if form.is_valid():
            log = form.save()
            material = Material.objects.get(id=log.material.id)
            log.qnt_em_estoque = material.qnt_em_estoque
            material.qnt_em_estoque = material.qnt_em_estoque+log.add_quantidade
            material.save()
            log.save()
            if log.add_quantidade == 1:
                messages.success(request, f"{log.add_quantidade} nova unidade adicionada ao estoque. Total: {material.qnt_em_estoque}.")
            else: 
                messages.success(request, f"{log.add_quantidade} novas unidades adicionadas ao estoque. Total: {material.qnt_em_estoque}.")
            return redirect('cevest_almoxarifado:index')
    else:
        form = Log_estoque_Form()
        form_tipo = Exibir_Tipo_Material_Form()

    context = {
        'titulo': apps.get_app_config('cevest_almoxarifado').verbose_name,
        'form': form,
        'tipos': Tipo_Material.objects.all(),
        'form_tipo': form_tipo
    }
    return render(request, 'cevest_almoxarifado/adicionar_material_ao_estoque.html', context)

def retirar_material_do_estoque(request, id):
    if request.method == 'POST':
        form = Log_estoque_Form(request.POST)
        form_tipo = Exibir_Tipo_Material_Form(request.POST)
        if form.is_valid():
            log = form.save()
            material = Material.objects.get(id=log.material.id)
            log.qnt_em_estoque = material.qnt_em_estoque
            material.qnt_em_estoque = material.qnt_em_estoque-log.add_quantidade
            material.save()
            log.save()
            if log.add_quantidade == 1:
                messages.success(request, f"{log.add_quantidade} unidade foi removida do estoque. Total: {material.qnt_em_estoque}.")
            else: 
                messages.success(request, f"{log.add_quantidade} unidades foram removidas do estoque. Total: {material.qnt_em_estoque}.")
            return redirect('cevest_os:detalhes_os', id)
    else:
        form = Log_estoque_Form(initial={'tipo_movimentacao': 'S'})
        form_tipo = Exibir_Tipo_Material_Form()

    context = {
        'titulo': apps.get_app_config('cevest_almoxarifado').verbose_name,
        'form': form,
        'tipos': Tipo_Material.objects.all(),
        'form_tipo': form_tipo
    }
    return render(request, 'cevest_almoxarifado/remover_material_ao_estoque.html', context)


@login_required
def listar_materiais(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        print(data)
        if not data['tipo']:
            return Exception("DEU MERDA, CADE O ID????")
        materiais = Material.objects.filter(tipo = data['tipo']).values()
        print(materiais)
        return JsonResponse({'data': list(materiais)})
    else:
        raise PermissionDenied()

@login_required
def historico(request):
    logs=Log_estoque.objects.all().order_by('id')
    context={
        'logs': logs
    }
    return render(request, 'cevest_almoxarifado/historico.html', context)