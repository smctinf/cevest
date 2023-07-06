from django.shortcuts import render
from django.apps import apps
from .models import Evento
from desenvolve_nf.models import Carousel_Index

def index(request):
    context={
        'titulo': apps.get_app_config('eventos').verbose_name,
        'eventos': Evento.objects.filter(is_destaque=True).order_by('data_inicio'),
        'carousel': Carousel_Index.objects.filter(ativa=True)
    }
    return render(request, "evento.html", context)

def evento_detalhe(request, id):
    evento=Evento.objects.get(id=id)
    context={
        'evento': evento,
        'titulo': apps.get_app_config('eventos').verbose_name,
        'categoria': apps.get_app_config(evento.app_name).verbose_name,
        'eventos': Evento.objects.filter(is_destaque=True),
        'carousel': Carousel_Index.objects.filter(ativa=True)
    }
    return render(request, "evento_detalhe.html", context)