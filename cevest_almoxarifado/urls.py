from django.urls import path
from . import views

app_name='cevest_almoxarifado'
urlpatterns = [
    path('', views.listar_tipo_materiais, name="index"),
    
    path('getMaterial/<int:id>/', views.getMaterial, name='get_material'),
    path('listar-tipo-materiais/', views.listar_tipo_materiais, name="alm_listar_tipos"),
    path('listar-materiais/', views.listar_materiais, name="alm_listar_materiais"),
    path('adicionar-tipo-materiais/', views.adicionar_tipo_materiais, name="alm_adicionar_tipo"),
    path('adicionar-material/<tipo>', views.adicionar_material, name="alm_adicionar_material"),
    path('adicionar-material-ao-estoque/', views.adicionar_material_ao_estoque, name="alm_adicionar_material_ao_estoque"),
    path('<id>/remover-material-do-estoque/', views.retirar_material_do_estoque, name="alm_remover_material_do_estoque"),
    path('historico/', views.historico, name="historico"),
    
]