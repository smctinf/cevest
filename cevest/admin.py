# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *


class CursoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'programa',
                    'duracao', 'dt_inclusao', 'exibir', 'ativo']
    list_filter = ['programa']
    search_fields = ['nome']


class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'carga_horaria')
    list_filter = ['nome']
    search_fields = ['nome']


class MatrizAdmin(admin.ModelAdmin):
    list_display = ('id', 'curriculo', 'curso', 'disciplina')
    list_filter = ['curso']
    search_fields = ['curso__nome', 'disciplina__nome']


class AlunoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cpf', 'celular', 'dt_inclusao')
    list_filter = ['cursos']
    filter_horizontal = ('cursos',)
    search_fields = ['nome']


class PresencaAdmin(admin.ModelAdmin):
    list_display = ('id', 'turma', 'aluno', 'data_aula')
    list_filter = ['turma']


class FeriadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'data')
    list_filter = ['data']


class BairroAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id', 'nome', 'cidade')
    list_filter = ['cidade']
    search_fields = ['nome']


class Turma_PrevistaAdmin(admin.ModelAdmin):
    list_display = ('id', 'curso', 'nome', 'curriculo',
                    'instrutor', 'dt_inicio', 'dt_fim', 'situacao')
    list_filter = ['curso']
    filter_horizontal = ('horario',)
    search_fields = ['curso__nome', 'instrutor__nome']


class Aluno_Turma_PrevistaAdmin(admin.ModelAdmin):
    list_display = ('id', 'turma_prevista', 'aluno',
                    'dt_inclusao', 'status_aluno_turma_prevista')
    list_filter = ['turma_prevista']
    search_fields = ['aluno__nome']


class Turma_Prevista_Turma_DefinitivaAdmin(admin.ModelAdmin):
    list_display = ('id', 'turma_prevista', 'turma', 'dt_inclusao')


class TurmaAdmin(admin.ModelAdmin):
    list_display = ('id', 'curso', 'nome', 'curriculo', 'instrutor',
                    'dt_inicio', 'dt_fim', 'situacao', 'exibir', 'dt_inclusao')
    list_filter = ['curso']
    filter_horizontal = ('horario',)
    search_fields = ['curso__nome', 'instrutor__nome']


class Aluno_TurmaAdmin(admin.ModelAdmin):
    list_display = ('id', 'turma', 'aluno', 'dt_inclusao', 'situacao')
    list_filter = ['turma']
    search_fields = ['aluno__nome']


admin.site.register(Curso, CursoAdmin)
admin.site.register(Disciplina, DisciplinaAdmin)
admin.site.register(Situacao)
admin.site.register(Presenca, PresencaAdmin)
admin.site.register(Feriado, FeriadoAdmin)
admin.site.register(Situacao_Turma_Definitiva)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Turno)
admin.site.register(Situacao_Turma)
admin.site.register(Bairro, BairroAdmin)
admin.site.register(Turma_Prevista, Turma_PrevistaAdmin)
admin.site.register(Aluno_Turma_Prevista, Aluno_Turma_PrevistaAdmin)
admin.site.register(Turma_Prevista_Turma_Definitiva,
                    Turma_Prevista_Turma_DefinitivaAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Horario)
admin.site.register(Aluno_Turma, Aluno_TurmaAdmin)
admin.site.register(Programa)
admin.site.register(Status_Aluno_Turma_Prevista)
admin.site.register(Pre_requisito)
admin.site.register(Curriculo)
admin.site.register(Matriz, MatrizAdmin)
admin.site.register(Instrutor)
admin.site.register(Cidade)
admin.site.register(Escolaridade)
admin.site.register(Profissao)
