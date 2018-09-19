from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('teste', views.teste, name='teste'),
]

# urlpatterns = patterns('',
#     url(r'^cevest/$', views.index, name='index'),
# )
