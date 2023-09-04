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
            messages.error(request, 'Usuário não encontrado')
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
                    subject = "Alteração de Senha do Sistema desenvolve da Secretária municipal de ciência e tecnologia de Nova Friburgo"
                    email_template_name = "adm/email_passwd_reset.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
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
                            user.save()

                        pessoa = form_pessoa.save(commit=False)
                        pessoa.user = user
                        pessoa.save()
                        user.first_name = pessoa.nome
                        user.username = pessoa.cpf
                        user.email = pessoa.email
                        user.save()
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
                            request, 'Email de usuário já cadastrado')
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

