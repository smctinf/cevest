from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from cursos.forms import Aluno_form

from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError

from cursos.models import Aluno
from .models import *
from .forms import *

from django.contrib.auth.decorators import login_required
from cursos.forms import Aluno_form
# Create your views here.

def change_email_for_cpf(request):
    pessoas = Pessoa.objects.all()
    response = 'Tudo certo!'
    for pessoa in pessoas:
        try:
            pessoa.user.username = pessoa.cpf
            pessoa.user.email = pessoa.email
            pessoa.user.save()
        except:
            response = 'Nem tudo são flores.'
            print('CEVEST_ERROR - ', pessoa.cpf, pessoa.email)
    return HttpResponse(response)

def login_view(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            pessoa = Pessoa.objects.get(cpf=username)
            user = authenticate(request, username=pessoa.cpf, password=password)
        except:
            try:
                pessoa = Pessoa.objects.get(email=username)
                user = authenticate(request, username=pessoa.cpf, password=password)
            except:   
                user=None
                redirect('/login')
            # user = authenticate(request, username=username.email, password=password)
   
        if user is not None:
            login(request, user)
            try:
                return redirect(request.GET['next'])
            except:
                return redirect('/')
        else:
            print(username, password)
            context = {
                'error': True,
            }
    return render(request, 'adm/login.html', context)

def passwd_reset(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "CEVEST - Alteração de Senha"
                    email_template_name = "adm/email_passwd_reset.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'CEVEST',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, user.email, [
                                  user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("autenticacao:passwd_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="adm/passwd_reset.html", context={"password_reset_form": password_reset_form})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/login')
    else:
        return redirect('/')

from django.contrib.auth.decorators import user_passes_test

@login_required
@user_passes_test(lambda u: u.is_superuser)
def adm_cadastro_user(request):
    if request.method == 'POST':
        try:
            pessoa=Pessoa.objects.get(cpf=request.POST['cpf'])
            messages.error(request, 'Usuário já cadastrado')
        except:
            pessoa = None
        if not pessoa:
            form = Form_Pessoa(request.POST)
            if form.is_valid():
                pessoa=form.save()
                partes=request.POST['dt_nascimento'].split('-')
                user = User.objects.create_user(username=str(validate_cpf(request.POST['cpf'])), first_name=request.POST['nome'] ,email=request.POST['email'] or None, password=partes[2] + partes[1] + partes[0])
                print(partes[2] + partes[1] + partes[0])
                pessoa.user=user
                pessoa.save()
                Aluno.objects.create(
                    pessoa=pessoa,
                    profissão='Não informado',
                    escolaridade='emc',
                    estado_civil='s',
                    aceita_mais_informacoes=True,
                    li_e_aceito_termos=True
                )
                # aluno.save()
                messages.success(request, 'Usuário cadastrado com sucesso!')
    else:
        form = Form_Pessoa()
    context = {
        'form': form
    }
                            
    return render(request, 'adm/adm_cadastro.html', context)   
 
def cadastro_user(request):
    
    form_pessoa = ''
    pessoa = ''
    is_user = False

    if request.user.is_authenticated:
        is_user = True

        try:
            pessoa = Pessoa.objects.get(user=request.user)
            form_pessoa = Form_Pessoa(initial={'email': request.user.email}, instance=pessoa)
            
        except Exception as e:
            form_pessoa = Form_Pessoa(initial={'email': request.user.email})
    else:
        form_pessoa = Form_Pessoa()
        form_aluno = Aluno_form()

    if request.method == "POST":
        if pessoa:
            form_pessoa = Form_Pessoa(request.POST, instance=pessoa)
        else:
            form_pessoa = Form_Pessoa(request.POST)
            form_aluno = Aluno_form(request.POST)

        if form_pessoa.is_valid():

            # com o objetivo de diminuir a identação, e não sendo possível utilizar guard clauses, optei em 
            # verificar o is_user duas vezes
            if is_user or request.POST['password'] == request.POST['password2']:
                if is_user or len(request.POST['password']) >= 8:
                    try:
                        user = ''                        
                        if is_user:
                            user = User.objects.get(id=request.user.id)
                            user.email = request.POST['email']
                            user.save()
                        else:                            
                            user = User.objects.create_user(username=str(validate_cpf(request.POST['cpf'])), email=request.POST['email'] or None, password=request.POST['password'])
                            

                        pessoa = form_pessoa.save()
                        pessoa.user = user
                        user.first_name = pessoa.nome
                        user.username = pessoa.cpf
                        user.email = pessoa.email
                        user.save()
                        pessoa.save()
                        aluno=form_aluno.save(commit=False)
                        aluno.pessoa = pessoa
                        aluno.save()
                        messages.success(
                            request, 'Usuário cadastrado com sucesso!')
                        try:
                            return redirect(request.GET['next'])
                        except:
                            return redirect('/login')
                    except Exception as e:
                        print('ERROR:', str(e))
                        messages.error(
                            request, 'Usuário já cadastrado')
                else:      
                    messages.error(
                    request, 'A senha deve possuir pelo menos 8 caracteres')
            else:
                # as senhas não se coincidem
                messages.error(request, 'As senhas digitadas não se coincidem')
    context = {
        'form_pessoa': form_pessoa,
        'is_user': is_user,
        'form_aluno': form_aluno
    }    
    return render(request, 'adm/cadastro.html', context)

@login_required
def cadastro_aluno(request):
    form_aluno = Aluno_form()
    pessoa = Pessoa.objects.get(user=request.user)

    if request.method == 'POST':
        form = Aluno_form(request.POST)
        if form.is_valid():
            aluno = form.save(commit=False)
            aluno.pessoa = pessoa
            aluno.save()

            messages.success(request, "Cadastro completo!")
            try:
                return redirect(request.GET['next'])
            except:
                return redirect('cursos:home')
            


    context = {
        'form': form_aluno
    }

    return render(request, 'adm/completar_cadastro.html', context)

def gambiarra_01(request):
    pessoas = Pessoa.objects.all()
    for pessoa in pessoas:
        try:
            pessoa.user.username = pessoa.cpf
            pessoa.user.save()
        except:
            print('USERNAME CEVEST_ERROR - ', pessoa.cpf)
        try:
            pessoa.user.email = pessoa.email
            pessoa.user.save()
        except:
            print('EMAIL CEVEST_ERROR - ', pessoa.cpf)
        try:
            pessoa.user.first_name = pessoa.nome
            pessoa.user.save()
        except: 
            print('FIRST_NAME CEVEST_ERROR - ', pessoa.cpf)
        try:
            aluno = Aluno.objects.get(pessoa=pessoa)
        except:
            try:
                aluno = Aluno(
                    pessoa = pessoa,
                    profissão = 'Não informado',
                    escolaridade = 'emc',
                    estado_civil = 's',
                    aceita_mais_informacoes = True,
                    li_e_aceito_termos = True,
                )
                aluno.save()
            except Exception as E:
                print(E)
                print(pessoa.cpf)
    return HttpResponse('Tudo certo!')