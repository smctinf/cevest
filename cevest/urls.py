from django.urls import path
from . import views

urlpatterns = [
    #Administrativo
    path('inicio', views.inicio, name='inicio'),
#     path('sair', views.sair, name='sair'),

#     path('alocados', views.alocados, name='alocados'),
#     path('portador', views.portador, name='portador'),

#     # TURMAS
#     path('turmas/confirmar', views.confirmar_turma, name='confirmar_turma'),
#     path('turmas/listar',views.listar_turmas, name = "listar_turmas"),

#     path('turma_prevista/<int:idcurso>', views.turma_prevista, name='turma_prevista'),


#     # SLA
#     path('recibo_ind', views.recibo_ind, name='recibo_individual'),
#     path('recibo_ind/<int:pk>', views.recibo_ind2, name='recibo_individual2'),
#     path('pauta', views.pauta, name='pauta'),
#     path('pauta2/<int:turma_id>', views.pauta2, name='pauta2'),

#     #Usuário
#     path('', views.index, name='index'),
#     path('index', views.index, name='index'),
#     path('cursos/<int:pk>', views.cursos, name='cursos'),
#     path('curso/<int:pk>', views.curso, name='curso'),
#     path('altera/<int:pk>', views.altera, name='altera'),
#     path('altera_cadastro',views.AlterarCadastro, name='altera_cadastro'),
#     path('detalhe', views.detalhe, name='detalhe'),
#     path('matriz/<int:idcurso>', views.matriz, name='matriz'),

#     path('get_bairro/<int:cidade_id>', views.get_bairro, name='get_bairro'),
#     path('resultado', views.resultado, name='resultado'),
#     path('lista_alocados',views.lista_alocados, name = "lista_alocados"),
#     path('indicadores',views.indicadores, name = "indicadores"),

#  # Teste
#     path('altera_cpf', views.altera_cpf, name='altera_cpf'),
#     #path('altera/<int:cpf>/<int:dt_nascimento>/', views.altera, name='altera'),
#     path('cadastro', views.cadastro, name='cadastro'),
#     path('teste', views.teste_ajax, name='teste'),
#     path('ajax/load_bairros/', views.load_bairros, name = 'ajax_load_bairros'),
]