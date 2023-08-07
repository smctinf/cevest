from django.contrib import admin
from django.urls import path
from . import views
 
app_name='cursos'
urlpatterns = [
    path('', views.index, name='home'),
    path('area-do-estudante/', views.area_do_estudante, name='area_do_estudante'),
    path('editar-cadastro/', views.editar_cadastro, name='editar_cadastro'),
    path('editar-senha/', views.alterar_senha, name='alterar_senha'),
    path('editar-cadastro-pessoa/', views.editar_cadastro_pessoa, name='editar_cadastro_pessoa'),
    path('atividade/<tipo>', views.cursos, name="cursos"),            
    path('atividade/<tipo>/<filtro>', views.cursos_filtrado, name="filtrar"),            
    path('atividade/<tipo>/<id>/detalhe', views.curso_detalhe, name="curso_detalhe"),            
    path('atividade/<tipo>/<id>/matricular', views.matricular, name="matricula"),            
    # path('prematricula/', views.prematricula, name="prematricula"),
    path('ensino-superior/', views.ensino_superior, name="ensino_superior"),
    path('ensino-tecnico/', views.ensino_tecnico, name="ensino_tecnico"),
    path('curriculo-vitae/', views.curriculo_vitae, name="curriculo_vitae"),
]