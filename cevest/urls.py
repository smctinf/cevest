from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('cursos', views.cursos, name='cursos'),
    path('cadastro', views.cadadastro, name='cadastro'),
    path('altera/<int:pk>', views.altera, name='altera'),
    path('detalhe', views.detalhe, name='detalhe'),
 
 # Teste
    path('altera_cpf', views.altera_cpf, name='altera_cpf'),
#    path('altera/<int:cpf>/<int:dt_nascimento>/', views.altera, name='altera'),
#    path('cadastro', views.cadastro, name='cadastro'),
#    path('teste', views.teste, name='teste'),
]

# urlpatterns = patterns('',
#     url(r'^cevest/$', views.index, name='index'),
# )
