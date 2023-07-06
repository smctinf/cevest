from django.urls import path
from . import views

app_name='eventos' 
urlpatterns = [
    path('', views.index, name="index"),
    path('evento/<id>', views.evento_detalhe, name="detalhe"),
]