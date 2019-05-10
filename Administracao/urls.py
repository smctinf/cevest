from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
    
app_name = 'administracao'
urlpatterns = [
    path('selecionar_turma_para_certificado', views.SelecionarTurmaParaCertificado, name='selecionar_turma_para_certificado'),
    path('gerar_certificados', views.GerarCertificados, name='gerar_certificados'),
    path('',views.AreaAdmin, name='area_admin'),
    path('index',views.AreaAdmin, name='area_admin'),
    path('corrigir_capitalizacao', views.capitalizar_nomes, name="capitalizar_nomes"),
    path('criar_feriados_moveis', views.criar_feriados_moveis, name = "criar_feriados_moveis"),
    path('selecionar_turma_para_alterar_situacao',views.SelecionarTurmaParaSituacao, name="selecionar_turma_para_alterar_situacao"),
    path('alterar_situacao_aluno',views.AlterarSituacaoAluno, name="alterar_situacao_aluno"),
    path('carregar_matriz_txt',views.AdicionarMatrizesDeTxT, name="carregar_matriz_txt"),
    path('selecionar_turma_para_presenca',views.SelecionarTurmaParaControle, name = "selecionar_turma_para_presenca"),
    path('escolher_dia_controle', views.EscolherDiaParaControle, name = "escolher_dia_controle"),
    path('controle_presenca',views.ControleDePresenca, name="controle_presenca"),
    path('login', auth_views.LoginView.as_view(template_name='cevest/login.html')),
    path('logout',views.logout_view,name="logout"),
    path('confirmar_turma', views.ConfirmarTurma, name="confirmar_turma"),
    path('bacalhau_arrumar_turma', views.ArrumarSituacaoTurmaBacalhau, name = 'bacalhau_arrumar_turma')
]