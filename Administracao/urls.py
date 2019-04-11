from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
    
app_name = 'administracao'
urlpatterns = [
    path('selecionar_turma_para_certificado', views.SelecionarTurmaParaCertificado, name='selecionar_turma_para_certificado'),
    path('gerar_certificados', views.GerarCertificados, name='gerar_certificados'),
    path('',views.AreaAdmin, name='area_admin'),
    path('corrigir_capitalizacao', views.capitalizar_nomes, name="capitalizar_nomes"),
    path('login', auth_views.LoginView.as_view(template_name='cevest/login.html')),
    path('logout',views.logout_view,name="logout"),
]