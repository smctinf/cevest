from django import template
from cursos.models import Alertar_Aluno_Sobre_Nova_Turma
register = template.Library()

@register.filter
def qntInteressados(id):
    return Alertar_Aluno_Sobre_Nova_Turma.objects.filter(curso=id).count()