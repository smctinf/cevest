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
    path('bacalhau_arrumar_turma', views.ArrumarSituacaoTurmaBacalhau, name = 'bacalhau_arrumar_turma'),
    path('escolher_turma_para_alocacao',views.EscolherTurmaPrevistaParaAlocacao, name = "escolher_turma_para_alocacao"),
    path('alocacao',views.Alocacao, name = 'alocacao'),
    path('escolher_turma_prevista_para_alterar_situacao',views.EscolherTurmaPrevistaParaAlterarSituacao, name = 'escolher_turma_prevista_para_alterar_situacao'),
    path('alterar_situacao_turma_prevista',views.AlterarSituacaoTurmaPrevista, name = 'alterar_situacao_turma_prevista'),
    path('confirmar_informacoes_aluno_previsto/<int:turma_id>/<int:aluno_id>/',views.ConfirmarInformacoesAlunoPrevisto, name = 'confirmar_informacoes_aluno_previsto'),
    path('lista_alocados_telefone',views.lista_alocados_telefone, name = "lista_alocados_telefone"),
    path('lista_alocados_telefone_zap',views.lista_alocados_telefone_zap, name = "lista_alocados_telefone_zap"),
    path('lista_alfabetica',views.lista_alfabetica, name = "lista_alfabetica"),
    path('lista_nao_alocados',views.lista_nao_alocados, name = "lista_nao_alocados"),
    path('lista_todos_por_curso_e_turno/<int:curso_id>/<int:turno_id>',views.lista_todos_por_curso_e_turno, name = "lista_todos_por_curso_e_turno"),
    path('quantidade_situacao_aluno_turma',views.quantidade_situacao_aluno_turma, name = "quantidade_situacao_aluno_turma"),
    path('quantidade_situacao_aluno_turma_prevista',views.quantidade_situacao_aluno_turma_prevista, name = "quantidade_situacao_aluno_turma_prevista"),
    path('alunos_formados_tel',views.alunos_formados_tel, name = "alunos_formados_tel"),
    path('ajuda',views.ajuda, name = "ajuda"),
    path('ajuda_funcionamento',views.ajuda_funcionamento, name = "ajuda_funcionamento"),
    path('ajuda_atualizacoes',views.ajuda_atualizacoes, name = "ajuda_atualizacoes"),
    path('lista_celular_por_turma/<str:turma_aberta>',views.lista_celular_por_turma, name = "lista_celular_por_turma"),
    path('lista_turmas_nao_fechadas',views.lista_turmas_nao_fechadas, name = "lista_turmas_nao_fechadas"),
    path('encerrar_turma',views.encerrar_turma, name = "encerrar_turma"),
    path('total_cadastrados_em_dado_periodo',views.total_cadastrados_em_dado_periodo, name = "total_cadastrados_em_dado_periodo"),

    ### Apagar
    path('apaga_costurareta',views.apaga_costurareta, name = "apaga_costurareta"),


    # Emitir Certificado
    path('selecionar_aluno_para_declaracao', views.SelecionarAlunoParaDeclaracao, name='selecionar_aluno_para_declaracao'),
    path('gerar_declaracao', views.GerarDeclaracao, name='gerar_declaracao'),

    path('change_password', views.change_password, name='change_password'),
]
