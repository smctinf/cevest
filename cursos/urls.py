from django.contrib import admin
from django.urls import path
from . import views
 
app_name='cursos'
urlpatterns = [
    path('', views.index, name='home'),
    path('atividade/<tipo>', views.cursos, name="cursos"),            
    path('atividade/<tipo>/<filtro>', views.cursos_filtrado, name="filtrar"),            
    path('atividade/<tipo>/<id>/detalhe', views.curso_detalhe, name="curso_detalhe"),            
    path('atividade/<tipo>/<id>/matricular', views.matricular, name="matricula"),            
    # path('prematricula/', views.prematricula, name="prematricula"),
    path('ensino-superior/', views.ensino_superior, name="ensino_superior"),
    path('ensino-tecnico/', views.ensino_tecnico, name="ensino_tecnico"),
    path('curriculo-vitae/', views.curriculo_vitae, name="curriculo_vitae"),

]