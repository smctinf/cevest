# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

# Status_Aluno_Turma_Prevista

from .models import Status_Aluno_Turma_Prevista
admin.site.register(Status_Aluno_Turma_Prevista)

from .models import Pre_requisito
admin.site.register(Pre_requisito)

from .models import Curriculo
admin.site.register(Curriculo)

from .models import Curso
admin.site.register(Curso)

from .models import Disciplina
admin.site.register(Disciplina)

from .models import Matriz
class MatrizAdmin(admin.ModelAdmin):
    # ...
    list_display = ('curriculo', 'curso', 'disciplina')
    list_filter = ['curso']

admin.site.register(Matriz, MatrizAdmin)

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
    list_display = ('nome', 'cpf', 'celular', 'dt_inclusao')
    list_filter = ['cursos']
    filter_horizontal = ('cursos',)

admin.site.register(Aluno, AlunoAdmin)


from .models import Turno
admin.site.register(Turno)

from .models import Situacao
admin.site.register(Situacao)

from .models import Bairro
class BairroAdmin(admin.ModelAdmin):
    # ...
    list_display = ('nome', 'cidade')
    list_filter = ['cidade']

admin.site.register(Bairro, BairroAdmin)

from .models import Turma_Prevista
class Turma_PrevistaAdmin(admin.ModelAdmin):
    # ...
    list_display = ('curso', 'nome', 'curriculo', 'instrutor', 'dt_inicio', 'dt_fim')
    list_filter = ['curso']
    filter_horizontal = ('horario',)

admin.site.register(Turma_Prevista, Turma_PrevistaAdmin)

from .models import Aluno_Turma_Prevista
class Aluno_Turma_PrevistaAdmin(admin.ModelAdmin):
    # ...
    list_display = ('turma_prevista', 'aluno', 'dt_inclusao', 'status_aluno_turma_prevista')
    list_filter = ['turma_prevista']

admin.site.register(Aluno_Turma_Prevista, Aluno_Turma_PrevistaAdmin)

from .models import Turma_Prevista_Turma_Definitiva
class Turma_Prevista_Turma_DefinitivaAdmin(admin.ModelAdmin):
    # ...
    list_display = ('turma_prevista', 'turma', 'dt_inclusao')
#    list_filter = ['turma_prevista']

admin.site.register(Turma_Prevista_Turma_Definitiva, Turma_Prevista_Turma_DefinitivaAdmin)

from .models import Turma
class TurmaAdmin(admin.ModelAdmin):
    # ...
    list_display = ('curso', 'nome', 'curriculo', 'instrutor', 'dt_inicio', 'dt_fim')
    list_filter = ['curso']
    filter_horizontal = ('horario',)

admin.site.register(Turma, TurmaAdmin)

from .models import Horario
admin.site.register(Horario)

from .models import Aluno_Turma

class Aluno_TurmaAdmin(admin.ModelAdmin):
    # ...
    list_display = ('turma', 'aluno', 'dt_inclusao','situacao')
    list_filter = ['turma']

admin.site.register(Aluno_Turma, Aluno_TurmaAdmin)
