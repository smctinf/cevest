from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
    
app_name = 'administracao'
urlpatterns = [

    # Você escolhe a turma e o cpf do aluno para vc emitir o certificado, mas não há indicação nenhuma se
    # o cpf inserido não fazer parte da turma
    path('selecionar_turma_para_certificado', views.SelecionarTurmaParaCertificado, name='selecionar_turma_para_certificado'),
    path('gerar_certificados', views.GerarCertificados, name='gerar_certificados'),
    path('',views.AreaAdmin, name='area_admin'),

    # Deveria ser parte da API, mas pega o nome de cada aluno e formata direitinho
    path('corrigir_capitalizacao', views.capitalizar_nomes, name="capitalizar_nomes"),
    # Você seleciona uma turma. Você será redirecionado para o "alterar_situacao_aluno" e poderá atualizar a situação
    # de cada aluno da turma. Muito legal!
    path('selecionar_turma_para_alterar_situacao',views.SelecionarTurmaParaSituacao, name="selecionar_turma_para_alterar_situacao"),
    path('alterar_situacao_aluno',views.AlterarSituacaoAluno, name="alterar_situacao_aluno"),

    # Esse aqui carrega o arquivo matrizes.txt que pode ser encontrado no root do projeto. É meio estranho que seja um arquivo txt
    # mas muito interessante que conseguiram carregar um arquivo como esse com relativamente poucas linhas
    path('carregar_matriz_txt',views.AdicionarMatrizesDeTxT, name="carregar_matriz_txt"),

    # Você escolhe uma turma para dar presença. vc será redirecionado para "escolher_dia_controle" e poderá escolher o dia
    # Nisso você será jogado para o "controle_presenca" e poderá dar presença individualmente para cada aluno
    path('selecionar_turma_para_presenca',views.SelecionarTurmaParaControle, name = "selecionar_turma_para_presenca"),
    path('escolher_dia_controle', views.EscolherDiaParaControle, name = "escolher_dia_controle"),
    path('controle_presenca',views.ControleDePresenca, name="controle_presenca"),

    # Transforma a turma prevista em turma definitiva, mas temos que dar um jeito nas turmas que n possuem turno
    path('confirmar_turma', views.ConfirmarTurma, name="confirmar_turma"),
    # muda o status de todas as turmas previstas para definitiva aparentemente
    path('bacalhau_arrumar_turma', views.ArrumarSituacaoTurmaBacalhau, name = 'bacalhau_arrumar_turma'),
    
    # Aqui que vai ficar o sistema de designar quem vai ficar em cada turma aparentemente
    path('escolher_turma_para_alocacao',views.EscolherTurmaPrevistaParaAlocacao, name = "escolher_turma_para_alocacao"),
    path('alocacao',views.Alocacao, name = 'alocacao'),

    path('escolher_turma_prevista_para_alterar_situacao',views.EscolherTurmaPrevistaParaAlterarSituacao, name = 'escolher_turma_prevista_para_alterar_situacao'),
    path('alterar_situacao_turma_prevista',views.AlterarSituacaoTurmaPrevista, name = 'alterar_situacao_turma_prevista'),

    path('confirmar_informacoes_aluno_previsto/<int:turma_id>/<int:aluno_id>/',views.ConfirmarInformacoesAlunoPrevisto, name = 'confirmar_informacoes_aluno_previsto'),
    
    # Sem dados para ser exibidos nesse, n sei oq faz :)
    path('lista_alocados_telefone',views.lista_alocados_telefone, name = "lista_alocados_telefone"),
    # cria um csv, acho que inclui todos as dados dos Alunos, só que as colunas estão em inglês
    path('lista_alocados_telefone_zap',views.lista_alocados_telefone_zap, name = "lista_alocados_telefone_zap"),
    # Exibe uma tabelinha com todos os alunos,cpf e as turmas que ele pertencer
    path('lista_alfabetica',views.lista_alfabetica, name = "lista_alfabetica"),
    # Exibe uma lista de todos os alunos que n possuirem turmas, mas a função usada para fazer isso é meio lentinha, melhor trocar
    # para um outer join
    path('lista_nao_alocados',views.lista_nao_alocados, name = "lista_nao_alocados"),
    # Exibe todos os candidatos inscritos em um determinado curso e que estão disponíveis para o turno especificado
    # Precisa ver se funciona com o turno sendo um manyToMany relationship
    path('lista_todos_por_curso_e_turno/<int:curso_id>/<int:turno_id>',views.lista_todos_por_curso_e_turno, name = "lista_todos_por_curso_e_turno"),
    
    # É um filtrozinho bem estilo "casa do trabalhador" mas os inputs n são de date, tem que mudar isso.
    # e exibir um gráfico tbm
    path('quantidade_situacao_aluno_turma',views.quantidade_situacao_aluno_turma, name = "quantidade_situacao_aluno_turma"),
    path('quantidade_situacao_aluno_turma_prevista',views.quantidade_situacao_aluno_turma_prevista, name = "quantidade_situacao_aluno_turma_prevista"),
    
    # aparentemente exibe a lista de alunos formados com o curso, turma, nome e telefone. Mas em vi em outra tabela que tinha mais de
    # 400 pessoas formadas. Acho que essa outra contagem é de "formados" e não "pessoas formadas"
    path('alunos_formados_tel',views.alunos_formados_tel, name = "alunos_formados_tel"),

    path('ajuda',views.ajuda, name = "ajuda"),
    path('ajuda_funcionamento',views.ajuda_funcionamento, name = "ajuda_funcionamento"),
    path('ajuda_atualizacoes',views.ajuda_atualizacoes, name = "ajuda_atualizacoes"),

    path('lista_celular_por_turma/<str:turma_aberta>',views.lista_celular_por_turma, name = "lista_celular_por_turma"),

    # Exibe a lista de turmas aparentemente ainda ativas. Essa é uma tela bem importante e precisa de ter um linkizinho para mais detalhes
    path('lista_turmas_nao_fechadas',views.lista_turmas_nao_fechadas, name = "lista_turmas_nao_fechadas"),
    path('encerrar_turma',views.encerrar_turma, name = "encerrar_turma"),
    path('total_cadastrados_em_dado_periodo',views.total_cadastrados_em_dado_periodo, name = "total_cadastrados_em_dado_periodo"),

    # Um hubzinho para escolher a tabela que vc deseja ver, no momento só tem cursos e um redirect para o django admin
    path('tabelas',views.tabelas, name = "tabelas"),

    # CRUD completinho de cursos
    path('cursos',views.cursos, name = "cursos"),
    path('curso_inclui',views.curso_inclui, name = "curso_inclui"),
    path('curso_altera/<int:id>',views.curso_altera, name = "curso_altera"),
    path('curso_exclui/<int:id>',views.curso_exclui, name = "curso_exclui"),
    path('curso/<int:id>',views.curso, name = "curso"),

    ### Apagar
    path('apaga_costurareta',views.apaga_costurareta, name = "apaga_costurareta"),

    # Emitir declaração
    # Aparentemene é para gerar uma declaração que a pessoa está inscrita
    path('selecionar_aluno_para_declaracao', views.SelecionarAlunoParaDeclaracao, name='selecionar_aluno_para_declaracao'),
    path('gerar_declaracao', views.GerarDeclaracao, name='gerar_declaracao'),

    # Autenticação
    path('login', auth_views.LoginView.as_view(template_name='cevest/login.html')),
    path('logout',views.logout_view,name="logout"),
    path('change_password', views.change_password, name='change_password'),
]
