import json
from django.http import Http404, HttpResponse

from .models import Cidade, Bairro
"""
def get_bairro(request, cidade_id):
    if request.is_ajax():
        bairros = Bairro.objects.filter(cidade_id=cidade_id).order_by('nome')
        bairros = [ bairro_serializer(bairro) for bairro in bairros ]

        return HttpResponse(json.dumps(bairros), content_type='application/json')
    else:
        raise Http404

def bairro_serializer(bairro):
    return {'id': bairro.pk, 'nome': bairro.nome}


def more_todo(request):
    if request.is_ajax():
        todo_items = ['Mow Lawn', 'Buy Groceries',]
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

"""