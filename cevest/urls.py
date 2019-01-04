from django.urls import path
from . import views

urlpatterns = [
    path('', views.aguarde, name='index'),
    path('index', views.index, name='index'),
    path('cursos', views.cursos, name='cursos'),
    path('curso/<int:pk>', views.curso, name='curso'),
    path('cadastro', views.cadadastro, name='cadastro'),
    path('altera/<int:pk>', views.altera, name='altera'),
    path('detalhe', views.detalhe, name='detalhe'),
    path('matriz/<int:idcurso>', views.matriz, name='matriz'),
    path('turma_prevista/<int:idcurso>', views.turma_prevista, name='turma_prevista'),

    path('get_bairro/<int:cidade_id>', views.get_bairro, name='get_bairro'),

 # Teste
    path('altera_cpf', views.altera_cpf, name='altera_cpf'),
#    path('altera/<int:cpf>/<int:dt_nascimento>/', views.altera, name='altera'),
#    path('cadastro', views.cadastro, name='cadastro'),
#    path('teste', views.teste, name='teste'),
]

# urlpatterns = patterns('',
#     url(r'^cevest/$', views.index, name='index'),
# )
