from django.urls import path, include
from . import views
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView

app_name='autenticacao'
urlpatterns = [
    path('change_email_for_cpf/', views.change_email_for_cpf, name='change_email_for_cpf'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('passwd_reset/', views.passwd_reset, name='passwd_reset'),
    path('passwd_reset_confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='passwd_reset_confirm'),
    path('passwd_reset_done/', PasswordResetDoneView.as_view(), name='passwd_reset_done'),
    path('passwd_reset_complete/', PasswordResetCompleteView.as_view(), name='passwd_reset_complete'),

    path('cadastro/', views.cadastro_user, name='cadastrar_usuario'),
    path('adm/cadastro/', views.adm_cadastro_user, name='adm_cadastrar_usuario'),
    path('cadastro_aluno/', views.cadastro_aluno, name='cadastrar_aluno'),


]