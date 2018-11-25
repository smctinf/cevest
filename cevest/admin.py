# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import Curso
admin.site.register(Curso)

from .models import Disciplina
admin.site.register(Disciplina)

from .models import Matriz
admin.site.register(Matriz)

from .models import Instrutor
admin.site.register(Instrutor)

from .models import Cidade
admin.site.register(Cidade)

from .models import Escolaridade
admin.site.register(Escolaridade)

from .models import Profissao
admin.site.register(Profissao)

from .models import Aluno
class AlunoAdmin(admin.ModelAdmin):
    # ...
    list_display = ('nome', 'cpf')
#    list_filter = ['cursos']
    filter_horizontal = ('cursos',)

admin.site.register(Aluno, AlunoAdmin)

from .models import Turno
admin.site.register(Turno)

from .models import Bairro
class BairroAdmin(admin.ModelAdmin):
    # ...
    list_display = ('nome', 'cidade')
    list_filter = ['cidade']

admin.site.register(Bairro, BairroAdmin)
