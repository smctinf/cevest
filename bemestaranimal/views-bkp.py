from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import *
from .forms import *
from .functions import generateToken
from django.apps import apps

# Create your views here.

# def aluno_required(view_func):
#     @wraps(view_func)
#     def wrapper(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             pessoa = ''
#             aluno = ''

#             try:
#                 pessoa = Pessoa.objects.get(user=request.user)
#             except Exception as e:
#                 return redirect("cadastrar_usuario")

#             try:
#                 aluno = Aluno.objects.get(pessoa=pessoa)
#             except Aluno.DoesNotExist:
#                 return redirect("cadastrar_aluno")

#         else:
#             return redirect(settings.LOGIN_URL)
        
#         return view_func(request, *args, **kwargs)
#     return wrapper

def cadastro_tutor(request):
    if request.user.is_authenticated:
        try:
            pessoa = Pessoa.objects.get(user_id=request.user.id)
            if pessoa:
                pass
        except:
            return redirect('bemestaranimal:cadastrar_usuario')
        try:
            tutor = Tutor.objects.get(pessoa_id=pessoa.id)
            verify = True
        except:
            verify = False

        if not verify:
            print(pessoa)
            form_tutor = Form_Tutor(initial={'pessoa':pessoa})
        else:
            return redirect('bemestaranimal:index')
    else:
        return redirect('cadastrar_usuario')
    if request.method == "POST":
        form_tutor = Form_Tutor(request.POST)
        if form_tutor.is_valid():
            form_tutor.save()
            return redirect('bemestaranimal:index')
    context={
        'form_tutor':form_tutor,
        'titulo': apps.get_app_config('bemestaranimal').verbose_name,
    }
    return render(request, 'autenticacao/completar-cadastro.html', context)



def index(request):
    context={
        'titulo': apps.get_app_config('bemestaranimal').verbose_name,
        'catalogo': Catalogo.objects.all()
    }
    return render(request, 'index.html', context)

@login_required
def area_tutor(request):
    try:
        pessoa = Pessoa.objects.get(user_id=request.user.id)
        tutor = Tutor.objects.get(pessoa_id=pessoa.id)
    except:
        messages.error(request, 'Você não é cadastrado como tutor!')
        return redirect('completar_cadastro')
    return render(request, 'tutor/area_tutor.html')

@login_required
def cadastrar_animal(request):
    try:
        pessoa = Pessoa.objects.get(user_id=request.user.id)
        tutor = Tutor.objects.get(pessoa_id=pessoa.id)
        animal_form = Form_Animal(initial={'tutor':tutor})
    except:
        messages.error(request, 'Você não é cadastrado como tutor!')
        return redirect('bemestaranimal:completar_cadastro')
    especie_form = Form_Especie()
    if request.method == "POST":
        animal_form = Form_Animal(request.POST, request.FILES)
        especie_form = Form_Especie(request.POST)
        if animal_form.is_valid() and especie_form.is_valid():
            animal = animal_form.save(commit=False)
            v_especie = especie_form.save(commit=False)
            especie, verify = Especie.objects.get_or_create(nome_especie=v_especie.nome_especie)
            animal.especie_id = especie.id
            animal.save()
            animal_form = Form_Animal(initial={'tutor':tutor})
            especie_form = Form_Especie()


    try:
        animais = Animal.objects.filter(tutor=tutor)
    except:
        animais = []
    context = {
        'animal_form': animal_form,
        'especie_form': especie_form,
        'animais':animais,
        'titulo': apps.get_app_config('bemestaranimal').verbose_name,
    }
    return render(request, 'tutor/animal_cadastro.html', context)

@login_required
def editar_animal(request, id):
    animal = Animal.objects.get(id=id)
    especie = Especie.objects.get(id=animal.especie_id)
    animal_form = Form_Animal(instance=animal)
    especie_form = Form_Especie(instance=especie)
    if request.method == "POST":
        especie_form = Form_Especie(request.POST, instance=especie)
        animal_form = Form_Animal(request.POST, instance=animal)
        if animal_form.is_valid() and especie_form.is_valid():
            animal_form.save(commit=False)
            try:
                Animal.objects.get(especie_id=especie.id)
                one = True
            except:
                one = False
            v_especie = especie_form.save(commit=False)
            especie, verify = Especie.objects.get_or_create(nome_especie=v_especie.nome_especie)
            animal.especie = especie
            animal.save()
            if one and request.POST['nome_especie'] != especie.nome_especie:
                try:
                    especie.delete()
                except:
                    pass
        return redirect('bemestaranimal:cadastrar_animal')               
    context = {
        'animal':animal,
        'animal_form': animal_form,
        'especie_form': especie_form,
        'titulo': apps.get_app_config('bemestaranimal').verbose_name,
    }
    return render(request, 'tutor/animal_editar.html', context)

@login_required
def deletar_animal(request, id):
    animal = Animal.objects.get(pk=id)
    animal.delete()
    return redirect('bemestaranimal:cadastrar_animal')

@login_required
def cadastrar_errante(request):
    errante_form = Form_Errante()
    especie_form = Form_Especie()

    context = {
        'errante_form': errante_form,
        'especie_form': especie_form,
        'titulo': apps.get_app_config('bemestaranimal').verbose_name,
    }
    if request.method == "POST":
        errante_form = Form_Errante(request.POST, request.FILES)
        especie_form = Form_Especie(request.POST)
        if errante_form.is_valid():
            if especie_form.is_valid():
                errante = errante_form.save(commit=False)
                v_especie = especie_form.save(commit=False)
                especie, verify = Especie.objects.get_or_create(nome_especie=v_especie.nome_especie)
                errante.especie = especie
                errante.save()

                return redirect('bemestaranimal:index')
    context = {
        'errante_form': errante_form,
        'especie_form': especie_form,
        'titulo': apps.get_app_config('bemestaranimal').verbose_name,
    }
    return render(request, 'adm/animal-errante-cadastro.html', context)

@login_required
def listar_tutor(request):
    qntd = Tutor.objects.all().count()
    tutores = Tutor.objects.annotate(num=Count('animal'))
    context = {
        'tutores':tutores,
        'qntd':qntd,
        'titulo': apps.get_app_config('bemestaranimal').verbose_name,
    }
    return render(request, 'adm/listar-tutores.html', context)

@login_required
def listar_animal_tutor(request, tutor_id):
    animais = Animal.objects.filter(tutor_id=tutor_id)
    tutor = Tutor.objects.get(pk=tutor_id).pessoa.nome
    context = {
        'animais':animais,
        'tutor':tutor,
        'titulo': apps.get_app_config('bemestaranimal').verbose_name,
    }
    return render(request, 'adm/listar-animais-tutor.html', context)

@login_required
def cad_infos_extras(request, tutor_id, animal_id):
    animal = Animal.objects.get(pk=animal_id)
    try:
        info = Informacoes_Extras.objects.get(animal=animal.id)
        if info:
            info_extras_form = Form_Info_Extras(instance=info)
    except:
        info_extras_form = Form_Info_Extras(initial={'animal':Animal.objects.get(pk=animal_id).id})
    context = {
        'info_extras_form':info_extras_form,
        'animal':animal,
        'titulo': apps.get_app_config('bemestaranimal').verbose_name,
    }
    if request.method == "POST":
        if info:
            info_extras_form = Form_Info_Extras(request.POST, instance=info)
        else:
            info_extras_form = Form_Info_Extras(request.POST)
        if info_extras_form.is_valid():
            info_extras_form.save()
    return render(request, 'adm/info-extra-cadastrar.html', context)

@login_required
def cad_catalogo_animal(request):
    animal_form = Form_Animal()
    especie_form = Form_Especie()
    animal_catalogo_form = Form_Catalogo()
    if request.method == "POST":
        especie_form = Form_Especie(request.POST)
        animal_form = Form_Animal(request.POST, request.FILES)
        animal_catalogo_form = Form_Catalogo(request.POST)
        if animal_form.is_valid() and especie_form.is_valid():
            animal = animal_form.save(commit=False)
            v_especie = especie_form.save(commit=False)
            especie, verify = Especie.objects.get_or_create(nome_especie=v_especie.nome_especie)
            animal.especie_id = especie.id
            animal.save()
            if animal_catalogo_form.is_valid():
                animal_adocao = animal_catalogo_form.save(commit=False)
                animal_adocao.animal=animal
                animal_adocao.save()
                messages.success(request, 'Animal cadastrado com sucesso!')
                animal_form = Form_Animal()
                especie_form = Form_Especie()
                animal_catalogo_form = Form_Catalogo()
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    context = {
        'animal_catalogo_form':animal_catalogo_form,
        'especie_form':especie_form,
        'animal_form':animal_form,
        'titulo': apps.get_app_config('bemestaranimal').verbose_name,

    }
    return render(request, 'catalogo/animal-catalogo-cadastrar.html', context)


def catalogo(request):
    catalogo = Catalogo.objects.all()
    context = {
        'catalogo':catalogo,
        'titulo': apps.get_app_config('bemestaranimal').verbose_name,
    }
    return render(request, 'catalogo/animal-catalogo.html', context)


def entrevistaAdocao(request, id):
    animal = Catalogo.objects.get(pk=id)
    entrevistaPrevia_Form = Form_EntrevistaPrevia(initial={'animal':animal})
    if request.method == "POST":
        entrevistaPrevia_Form = Form_EntrevistaPrevia(request.POST)
        if entrevistaPrevia_Form.is_valid():
            entrevistaPrevia_Form.save()
            messages.success(request, 'Uma orientação?')
            return redirect('bemestaranimal:index')
    context = {
        'entrevistaPrevia_Form': entrevistaPrevia_Form,
        'adocao':animal,
        'titulo': apps.get_app_config('bemestaranimal').verbose_name,
    }
    return render(request, 'catalogo/entrevista.html', context)
    

@login_required
def gerarToken(request):
    #pra conseguir só os tutores que tem animal cadastrado
    
    tutores = Tutor.objects.all()
    count_s = 0
    count_n = 0
    for tutor in tutores:
        if len(Animal.objects.filter(tutor=tutor))!=0:
            try:
                TokenDesconto.objects.get(tutor=tutor)
            except:
                token = generateToken(tutor.id)
                new = TokenDesconto.objects.create(token=token, tutor=tutor)
                new.save()
                count_s += 1
        else:
            count_n += 1
    context = {
        'tutor_animal':count_s,
        'tutor_s_animal':count_n,
        'titulo': apps.get_app_config('bemestaranimal').verbose_name,
    }
    return render(request, 'adm/gerar-token.html', context)

    return render()

@login_required
def resgatar_cupom(request):
    pessoa = Pessoa.objects.get(user_id=request.user.id)
    tutor = Tutor.objects.get(pessoa_id=pessoa.id)
    try:
        cupom = TokenDesconto.objects.get(tutor=tutor)
    except:
        messages.error(request, 'Cupom não disponibilizado.')
        return render(request, 'tutor/area_tutor.html')
    context = {
        'cupom':cupom
    }
    return render(request, 'tutor/resgatar-token.html', context)

# @login_required
# def descontarToken(request):
#     if request.method == 'POST':
#         token = request.POST['token']
#         print(token)
#         try:
#             verify = TokenDesconto.objects.get(token=token)
#         except:
#             messages.error(request, 'Código promocional inválido.')
#             return render(request, 'adm/descontar-token.html')
#         if verify.used:
#             messages.error(request, 'Código promocional já utilizado.')
#         else:
#             verify.used = True
#             verify.save()
#             messages.success(request, 'Código promocional ativado com sucesso!')
#     return render(request, 'adm/descontar-token.html', {'titulo': apps.get_app_config('bemestaranimal').verbose_name,})

# def teste(request):
#     return render(request, 'adm/administracao.html')

#quantidade de animais castrados e não castrados
# vacinados (mas não pede essa informação no usuário, só na hora de cadastrar as informações extras)