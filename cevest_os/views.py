from django.shortcuts import render, redirect
from .forms import *
from autenticacao.models import Pessoa
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.apps import apps
from .models import *
from settings.decorators import group_required
from django.contrib.auth.models import Group
from datetime import datetime
from django.db.models import Count, Sum

STATUS_CHOICES=(
        ('0','Novo'),
        ('1','Aguardando'),
        ('2','Em execução'),
        ('f','Finalizado')
    )
PRIORIDADE_CHOICES=(
        ('0','Normal'),
        ('1','Moderada'),
        ('2','Urgente'),
    )

@group_required('cevest_os_acesso')
def index(request):
    return render(request, 'os_index.html')

@login_required
@group_required('cevest_os_acesso')
def os_painel(request):    
    meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    bairros = CEVEST_OrdemDeServico.objects.values_list('bairro', flat=True).distinct()
    data = []
    
    for bairro in bairros:
        total=CEVEST_OrdemDeServico.objects.filter(bairro=bairro, status__in=['0', '1', '2'], dt_solicitacao__year='2023').count()
        os_por_mes =CEVEST_OrdemDeServico.objects.filter(bairro=bairro, status__in=['0', '1', '2'], dt_solicitacao__year='2023').annotate(
            jan=Count('id', filter=models.Q(dt_solicitacao__month=1)),
            fev=Count('id', filter=models.Q(dt_solicitacao__month=2)),
            mar=Count('id', filter=models.Q(dt_solicitacao__month=3)),
            abr=Count('id', filter=models.Q(dt_solicitacao__month=4)),
            mai=Count('id', filter=models.Q(dt_solicitacao__month=5)),
            jun=Count('id', filter=models.Q(dt_solicitacao__month=6)),
            jul=Count('id', filter=models.Q(dt_solicitacao__month=7)),
            ago=Count('id', filter=models.Q(dt_solicitacao__month=8)),
            set=Count('id', filter=models.Q(dt_solicitacao__month=9)),
            out=Count('id', filter=models.Q(dt_solicitacao__month=10)),
            nov=Count('id', filter=models.Q(dt_solicitacao__month=11)),
            dez=Count('id', filter=models.Q(dt_solicitacao__month=12)),
        ).values('jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez')

        data.append({'bairro': bairro, 'mes': os_por_mes, 'total': total})

    
    # if request.method=='POST':
    #     pass

    
    context={
        'titulo': apps.get_app_config('cevest_os').verbose_name,
        'data': data,        
    }
    return render(request, 'cevest_os/painel.html', context)

@login_required
@group_required('cevest_os_acesso')
def os_index(request):
    if request.user.is_superuser:
        data=CEVEST_OrdemDeServico.objects.all()
    else:
        data=CEVEST_OrdemDeServico.objects.filter(atendente=Pessoa.objects.get(user=request.user))
    if request.method=='POST':
        valor_da_busca=request.POST['valor_da_busca']
        tipo=request.POST['tipo_da_busca']
        # print(valor_da_busca, tipo)
        if tipo == 'atendente':
            if valor_da_busca=='':
                data=data.filter(atendente=None)
            else:
                data=data.filter(atendente__first_name__icontains=valor_da_busca)
        elif tipo == 'bairro':
            data=data.filter(bairro__icontains=valor_da_busca)
        elif tipo == 'data':
            try:
                valor_da_busca_date = datetime.strptime(valor_da_busca, '%d/%m/%Y').date()            
                data=data.filter(dt_solicitacao__date=valor_da_busca_date.strftime('%Y-%m-%d'))
            except:
                valores=valor_da_busca.split('/')
                # print(valores)
                data=data.filter(dt_solicitacao__year=valores[1], dt_solicitacao__month=valores[0])
        elif tipo == 'protocolo':
            data=data.filter(numero__icontains=valor_da_busca)
        elif tipo == 'rua':
            data=data.filter(logradouro__icontains=valor_da_busca)
        elif tipo == 'status':
            status={'Novo': 0,
            'Aguardando': 1,
            'Em execução': 2,
            'Finalizado': 3}
            data=data.filter(status=status[valor_da_busca.capitalize()])
        elif tipo == 'prioridade':
            prioridades={'Normal': 0,
            'Moderada': 1,
            'Urgente': 2
            }
            data=data.filter(prioridade=prioridades[valor_da_busca.capitalize()])

    paginator = Paginator(data, 30)
    page = request.GET.get('page', 1)
    ordens_de_servico = paginator.get_page(page)
    
    context={
        'titulo': apps.get_app_config('cevest_os').verbose_name,
        'ordens_de_servico': ordens_de_servico
    }
    return render(request, 'cevest_os/index.html', context)


@login_required
def add_os(request):
    
    form = OS_Form(initial={'tipo': CEVEST_Tipo_OS.objects.get(sigla='TST').id})

    if request.method=='POST':
        form=OS_Form(request.POST)
        if form.is_valid():
            os=form.save(commit=False)
            os.cadastrado_por=Pessoa.objects.get(user=request.user)
            os.save()

            return redirect('cevest_os:os_index')                

    context={
        'titulo': apps.get_app_config('cevest_os').verbose_name,
        'form': form,
    }

    return render(request, 'cevest_os/adicionar_os.html', context)


def detalhes_os(request, id):
    pessoa = Pessoa.objects.get(user=request.user)
    os = CEVEST_OrdemDeServico.objects.get(id=id)
    form_mensagem = NovaMensagemForm(initial={'os': os.id, 'pessoa': pessoa.id})
    try:
        os_ext=CEVEST_OS_ext.objects.get(os=os)        
    except:
        os_ext = None         
    if request.method=='POST': 
        form_mensagem=NovaMensagemForm(request.POST, request.FILES)
        if form_mensagem.is_valid():
           msg=form_mensagem.save(commit=False)
           msg.os=os
           msg.pessoa=pessoa
           msg.save()
           form_mensagem = NovaMensagemForm(initial={'os': os.id, 'pessoa': pessoa.id})       

    linha_tempo=CEVEST_OS_Linha_Tempo.objects.filter(os=os)
    context={
        'form_mensagem': form_mensagem,
        'linha_tempo': linha_tempo,
        'STATUS': STATUS_CHOICES,
        'PRIORIDADES': PRIORIDADE_CHOICES, 
        'titulo': apps.get_app_config('cevest_os').verbose_name,
        'os': os,
        'os_ext': os_ext
    }
    return render(request, 'cevest_os/detalhes_os.html', context)

@group_required('cevest_os_acesso', 'cevest_os_funcionario')
def change_status_os(request, id, opcao):
    os=CEVEST_OrdemDeServico.objects.get(id=id)
    os.status=opcao
    if opcao=='f':
        os.dt_conclusao=datetime.now()
    os.save()
    return redirect('cevest_os:detalhes_os', id=id)

@group_required('cevest_os_acesso', 'cevest_os_funcionario')
def change_prioridade_os(request, id, opcao):
    os=CEVEST_OrdemDeServico.objects.get(id=id)
    os.prioridade=opcao
    os.save()
    return redirect('cevest_os:detalhes_os', id=id)

@group_required('cevest_os_acesso', 'cevest_os_funcionario')
def atender_os(request, id):
    os=CEVEST_OrdemDeServico.objects.get(id=id)
    os.atendente=request.user
    os.save()
    return redirect('cevest_os:detalhes_os', id=id)

@group_required('cevest_os_acesso', 'cevest_os_funcionario')
def funcionarios_listar(request):
    funcionarios=Funcionario_CEVEST_OS.objects.all()
    context={
        'titulo': apps.get_app_config('cevest_os').verbose_name,
        'funcionarios': funcionarios
    }
    return render(request, 'equipe/funcionarios.html', context)

@group_required('cevest_os_acesso', 'cevest_os_funcionario')
def funcionario_cadastrar(request):
    if request.method=='POST':
        form=Funcionario_Form({'pessoa':request.POST['pessoa'], 'nivel': request.POST['nivel'], 'tipo_os': [1]})
        if form.is_valid():
            form.save()
            funcionario=Funcionario_CEVEST_OS()
            return redirect('cevest_os:funcionarios')
        # else:
            # print(form.errors)
    else:
        form=Funcionario_Form(initial={'tipo_os': CEVEST_Tipo_OS.objects.get(sigla='IP')})
    context={
        'titulo': apps.get_app_config('cevest_os').verbose_name,
        'form': form
    }
    return render(request, 'equipe/funcionarios_cadastrar.html', context)

@group_required('cevest_os_acesso', 'cevest_os_funcionario')
def funcionario_editar(request, id):
    funcionario=Funcionario_CEVEST_OS.objects.get(id=id)
    form=Funcionario_Form_editar(instance=funcionario)
    if request.method=='POST':
        form=Funcionario_Form_editar(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('funcionarios')
    context={
        'titulo': apps.get_app_config('cevest_os').verbose_name,
        'form': form,
        'funcionario': funcionario
    }     
    return render(request, 'equipe/funcionarios_editar.html', context)

@group_required('cevest_os_acesso', 'cevest_os_funcionario')
def funcionario_deletar(request, id):
    funcionario=Funcionario_CEVEST_OS.objects.get(id=id)
    funcionario.delete()

    return redirect('cevest_os:funcionarios')

@group_required('cevest_os_acesso', 'cevest_os_funcionario')
def atribuir_equipe(request, id):
    try:
        instancia=CEVEST_OS_ext.objects.get(os=id)
        form=Equipe_Form(instance=instancia)        
    except Exception as e:
        form=Equipe_Form(initial={'os': id})
        instancia=None
        
    if request.method=='POST':
        if instancia:
            form=Equipe_Form(request.POST, instance=instancia)
        else:
            form=Equipe_Form(request.POST)
        if form.is_valid:
            form.save()
            return redirect('cevest_os:detalhes_os', id)
    context={
            'titulo': apps.get_app_config('cevest_os').verbose_name,   
            'form':form,
        }
    return render(request, 'cevest_os/adicionar_ext.html', context)

@group_required('cevest_os_acesso', 'cevest_os_funcionario')
def pontos_os(request, id):
    instancia=CEVEST_OrdemDeServico.objects.get(id=id)
    form=OS_Form_Ponto(instance=instancia)            
        
    if request.method=='POST':       
        form=OS_Form_Ponto(request.POST, instance=instancia)
        if form.is_valid:
            form.save()
            return redirect('cevest_os:detalhes_os', id)
    context={
            'titulo': apps.get_app_config('cevest_os').verbose_name,   
            'form':form,
        }
    return render(request, 'cevest_os/adicionar_ext.html', context)

from django.db.models import Count

def imprimir_os(request, id):
    lista_de_os=[CEVEST_OrdemDeServico.objects.get(id=id)]
    context={
        'lista_de_os': lista_de_os
    }
    return render(request, 'cevest_os/imprimir_os.html', context)

def imprimir_varias_os(request, ids):
    ids=ids.split('-')
    ids.pop()
    lista_de_os=[]
    for i in ids:
        lista_de_os.append(CEVEST_OrdemDeServico.objects.get(id=i))
    # print(len(lista_de_os))
    # print(ids)
    context={
        'lista_de_os': lista_de_os
    }
    return render(request, 'cevest_os/imprimir_os.html', context)

def graficos(request):
    pontos_por_bairro = CEVEST_OrdemDeServico.objects.values('bairro').annotate(total=Sum('pontos_atendidos')).order_by('-total')[:10]
    os_por_bairro = CEVEST_OrdemDeServico.objects.values('bairro').annotate(total=Count('id')).order_by('-total')[:10]
    finalizados = CEVEST_OrdemDeServico.objects.filter(status='f').count()
    nao_finalizados = CEVEST_OrdemDeServico.objects.exclude(status='f').count()
    os_por_funcionario = Funcionario_CEVEST_OS.objects.annotate(total=Count('id')).order_by('-total')[:10]
    context = {
        'pontos_por_bairro': pontos_por_bairro,
        'os_por_bairro': os_por_bairro,
        'finalizados': finalizados,
        'nao_finalizados': nao_finalizados,
        'os_por_funcionario': os_por_funcionario,
        'titulo': apps.get_app_config('cevest_os').verbose_name,
    }
    return render(request, 'cevest_os/graficos.html', context)