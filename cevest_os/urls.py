from django.urls import path
from . import views
 
app_name='cevest_os'
urlpatterns = [
    # path('', views.index, name='os_index'),
    path('', views.os_index, name='os_index'),
    path('painel/', views.os_painel, name='os_painel'),
    path('os/', views.add_os, name='add_os'),

    path('os/painel/<id>/', views.detalhes_os, name='detalhes_os'),
    path('os/painel/<id>/pontos', views.pontos_os, name='pontos_os'),
    path('imprimir/', views.os_index, name='imprimir_nada'),
    path('imprimir/<ids>/', views.imprimir_varias_os, name='imprimir_varias'),
    path('os/painel/<id>/imprimir/', views.imprimir_os, name='imprimir'),
    path('os/painel/<id>/alterar_status/<opcao>', views.change_status_os, name='change_status_os'),
    path('os/painel/<id>/alterar_prioridade/<opcao>', views.change_prioridade_os, name='change_prioridade_os'),
    path('os/painel/<id>/atender', views.atender_os, name='atender_os'),

    path('os/kpi', views.graficos, name='kpi'),
    path('funcionario', views.funcionarios_listar, name='funcionarios'),
    path('funcionario/cadastrar/', views.funcionario_cadastrar, name='cadastrar funcionario'),
    path('funcionario/editar/<id>/', views.funcionario_editar, name='editar funcionario'),
    path('funcionario/deletar/<id>/', views.funcionario_deletar, name='deletar funcionario'),

    path('os/painel/<id>/equipe/', views.atribuir_equipe, name='atribuir equipe')
]