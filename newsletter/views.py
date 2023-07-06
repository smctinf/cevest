from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'newsletter/index.html')

def solicitacao(request):
    return render(request, 'newsletter/solicitacao.html')