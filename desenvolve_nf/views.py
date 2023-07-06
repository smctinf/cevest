from django.shortcuts import render
from .models import Carousel_Index
from .models import ClimaTempo
from .functions import ClimaTempoTemperaturas


# Create your views here.
def index(request):
    context = {
        'carousel': Carousel_Index.objects.filter(ativa=True)
    }
    return render(request, 'index_desenvolvenf.html', context)

def getClimaTempo(request):
    #processos
    ClimaTempoTemperaturas()
    
    #fim de processos
    context={

    }
    return render(request, 'cidade_inteligente.html', context)

def cidade_inteligente_home(request):
    clima = ClimaTempo.objects.first()
    print(clima.turno())
    context = {
        'titulo': 'Cidade Inteligente',
        'clima': clima
    }
    return render(request, 'cidade_inteligente.html', context)