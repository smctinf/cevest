from django.urls import path
from . import views

app_name = 'newsletter'
urlpatterns = [
    path('', views.index, name='index'),
    path('solicitacao/', views.solicitacao, name='solicitacao'),
]
