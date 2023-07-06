from django.contrib import admin
from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.administrativo, name="administrativo2"),

    path('instiuicoes', views.adm_instituicoes_listar, name="adm_instituicoes_listar"),
    path('instituicao/cadastrar', views.adm_instituicao_cadastrar, name="adm_cadastrar_instituicao"),
    path('instituicao/<id>', views.adm_locais_editar, name="adm_editar_instituicao"),
    path('instituicao/<id>/excluir', views.adm_locais_excluir, name="adm_locais_excluir"),
    # MISSING EDITAR 

    path('locais', views.adm_locais_listar, name="adm_locais_listar"),
    path('local/cadastrar', views.adm_locais_cadastrar, name="cadastrar_local"),
    path('local/<id>/editar', views.adm_locais_editar, name="adm_locais_editar"),
    path('locai/<id>/excluir', views.adm_locais_excluir, name="adm_locais_excluir"),
    # MISSING VISUALIZAR

    path('categorias', views.adm_categorias_listar, name="adm_categorias_listar"),
    path('categoria/cadastrar', views.adm_categorias_cadastrar, name="cadastrar_categoria"),
    path('categoria/<id>/editar', views.adm_categorias_editar, name="adm_categorias_editar"),
    path('categoria/<id>/excluir', views.adm_categorias_excluir, name="adm_categorias_excluir"),
    # MISSING VISUALIZAR

    path('cursos', views.adm_cursos_listar, name="adm_cursos_listar"),
    path('curso/cadastrar', views.adm_cursos_cadastrar, name="adm_cursos_cadastrar"),
    path('curso/<id>/editar', views.adm_curso_editar, name="adm_curso_editar"),
    path('curso/<id>/visualizar', views.adm_curso_visualizar, name="adm_curso_visualizar"),
    # path('curso/<id>/requisito/criar', views.adm_curso_visualizar, name="adm_curso_visualizar"),


    # MISSING VISUALIZAR e EXCLUIR

    path('instrutores', views.adm_professores_listar, name="adm_professores_listar"),        
    path('instrutor/cadastrar', views.adm_professores_cadastrar, name="adm_professores_cadastrar"),
    path('instrutor/<id>/editar', views.adm_professores_editar, name="adm_professores_editar"),
    path('instrutor/<id>/excluir', views.adm_professores_excluir, name="adm_professores_excluir"),
    # MISSING VISUALIZAR

    # -------- Serve para confirmar um aluno selecionado, transformando seu status para "Aluno" -------- #
    path('selecionado/<matricula>', views.visualizar_turma_selecionado, name="adm_turma_visualizar_selecionado"),
    # -------- # -------- #

    path('turmas', views.adm_turmas_listar, name="adm_turmas_listar"),
    path('turma/cadastrar', views.adm_turmas_cadastrar, name="adm_turmas_cadastrar"),
    path('turma/<id>', views.adm_turmas_visualizar, name="adm_turma_visualizar"),
    path('turma/<id>/editar', views.visualizar_turma_editar, name="adm_turma_editar"),
    path('turma/<id>/excluir', views.excluir_turma, name="adm_turma_excluir"),
    path('turma/<id>/realocar', views.adm_realocar, name="adm_turma_realocar"),

    path('turma/<id>/turno/cadastrar', views.adm_turno_cadastrar, name="adm_turno_cadastrar"),
    # MISSING VISUALIZAR, EDITAR, LISTAR E EXCLUIR

    path('turma/<turma_id>/aula/cadastrar', views.adm_aula_cadastrar, name="adm_aula_cadastrar"),
    path('turma/<turma_id>/aulas', views.adm_aulas_listar, name="adm_aulas_listar"),
    path('turma/<turma_id>/aula/<aula_id>', views.adm_aula_visualizar, name="adm_aula_visualizar"),
    # MISSING EDITAR E EXCLUIR

    
    path('justificativa/<presenca_id>/cadastrar', views.adm_justificativa_cadastrar, name="adm_justificativa_cadastrar"),
    path('justificativa/<presenca_id>', views.adm_justificativa_visualizar, name="adm_justificativa_visualizar"),
    # MISSING LISTAR, EDITAR E EXCLUIR

    path('eventos', views.adm_eventos_listar, name="adm_eventos_listar"),
    path('evento/cadastrar', views.adm_evento_cadastrar, name="adm_evento_cadastrar"),
    path('evento/<id>/editar', views.adm_evento_editar, name="adm_evento_editar"),

    path('alunos', views.adm_alunos_listar, name="adm_alunos_listar"),
    path('aluno/<id>', views.adm_aluno_visualizar, name="adm_aluno_visualizar"),
    path('aluno/<id>/editar', views.adm_aluno_editar, name="adm_aluno_editar"),
    path('aluno/<matricula>/desmatricular', views.desmatricular_aluno, name="adm_desmatricular_aluno"),

    path('csv', views.import_users_from_csv),
    #####

    path('bem-estar-animal/animal/cadastrar-errante', views.cadastrar_errante, name='cadastrar_errante'),
    path('bem-estar-animal/animal/listar-errante', views.listar_errante, name='listar_errantes'),

    #tutor
    path('bem-estar-animal/tutor/', views.listar_tutor, name='listar_tutor'),
    path('bem-estar-animal/tutor/<tutor_id>/animais/', views.listar_animal_tutor, name='listar_animais_tutor'),
    path('bem-estar-animal/tutor/<tutor_id>/animais/<animal_id>', views.cad_infos_extras, name='cadastrar_info'),

    #catalogo
    path('bem-estar-animal/catalogo/cadastrar', views.cad_catalogo_animal, name='cadastrar_catalogo'),
    path('bem-estar-animal/entrevista-previa/', views.listar_entrevistas, name='listar_entrevistas'),
    path('bem-estar-animal/entrevista-previa/<id>', views.questionario, name='questionario'),

    # path desativar animal do catalogo

    #token
    path('bem-estar-animal/gerar-token', views.gerarToken, name='gerar_token'),
    path('bem-estar-animal/descontar-token', views.descontarToken, name='descontar_token'),

    #adm
    path('bem-estar-animal/', views.administrativo_bemestaranimal, name='administrativo'),
    path('bem-estar-animal/censo/', views.censo, name='censo')
]