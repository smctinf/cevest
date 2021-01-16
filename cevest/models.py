# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from .functions import validate_CPF

# Create your models here.


class Pre_requisito(models.Model):
    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Pré-Requisito"
#        verbose_name_plural = "Matrizes"
        ordering = ('descricao',)

    descricao = models.CharField(unique=True, max_length=100)
#    atende = models.BooleanField(default=False)

class Escolaridade(models.Model):
    def __str__(self):
        return self.descricao

    class Meta:
        ordering = ('descricao',)

    descricao = models.CharField(unique=True, max_length=50)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

class Curriculo(models.Model):
    def __str__(self):
        return self.nome

    class Meta:
        ordering = ('dt_fim', 'nome',)

    nome = models.CharField(max_length=30)
    dt_inicio = models.DateField('Data Início')
    dt_fim = models.DateField('Data Fim', blank=True, null=True)
    dt_inclusao = models.DateTimeField(auto_now_add=True)


class Programa(models.Model):
    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']

    nome = models.CharField(unique=True, max_length=50)
    ativo = models.BooleanField(default=True)
    dt_inclusao = models.DateTimeField(auto_now_add=True)


class Curso(models.Model):
    def __str__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)

    nome = models.CharField(max_length=80)
    descricao = models.TextField(max_length=2000)
    programa = models.ForeignKey(Programa, on_delete=models.PROTECT, default = 1)
    duracao = models.PositiveSmallIntegerField(default = 0)
    idade_minima = models.PositiveSmallIntegerField(default = 0)
    escolaridade_minima = models.ForeignKey(Escolaridade, on_delete=models.PROTECT, default = 1)
    pre_requisito = models.ManyToManyField(Pre_requisito, blank=True)
    quant_alunos = models.PositiveSmallIntegerField(default=0)
    dt_inclusao = models.DateTimeField(auto_now_add=True)
    exibir = models.BooleanField(default=True)
    ativo = models.BooleanField(default=True)

class Disciplina(models.Model):
    def __str__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)

    nome = models.CharField(max_length=100)
    carga_horaria = models.PositiveSmallIntegerField(default = 0)

class Matriz(models.Model):
    class Meta:
        verbose_name_plural = "Matrizes"

    def __int__(self):
        return '%s - %s - %s' % (self.curriculo, self.curso, self.disciplina)

    curriculo = models.ForeignKey(Curriculo, on_delete=models.PROTECT, default=True)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT)
    num_aulas = models.PositiveSmallIntegerField()
    carga_horaria_total = models.PositiveSmallIntegerField()

class Instrutor(models.Model):
    class Meta:
        verbose_name_plural = "Instrutores"
        ordering = ('nome',)

    def __str__(self):
        return self.nome

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    nome = models.CharField(max_length=60)
    matricula = models.CharField(unique = True, null = True, max_length=11) 
    dt_inclusao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

class Cidade(models.Model):
    def __str__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)

    nome = models.CharField(unique=True, max_length=30)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

class Bairro(models.Model):
    def __str__(self):
        return '%s' % (self.nome)

    class Meta:
        ordering = ('cidade', 'nome',)

    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    nome = models.CharField(unique=True, max_length=30)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

class Turno(models.Model):
    def __str__(self):
        return self.descricao

    descricao = models.CharField(max_length=50)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

class Profissao(models.Model):
    class Meta:
        verbose_name_plural = "Profissões"
        ordering = ('nome',)

    def __str__(self):
        return self.nome

    nome = models.CharField(max_length=50)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

SEXO = (
    ('F', 'Feminino'),
    ('M', 'Masculino'),
)

class Aluno(models.Model):
    def __str__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)

    nome = models.CharField(max_length=60)
    email = models.EmailField(max_length=254, blank=True, null=True)
    cpf = models.CharField(unique=True, max_length=11, validators=[validate_CPF])
    nis = models.CharField(unique=True, max_length=11, blank = True, null=True)
    bolsa_familia = models.BooleanField(default=False)
    quant_filhos = models.PositiveSmallIntegerField(default=0)
    sexo = models.CharField(max_length=1, choices=SEXO)
    portador_necessidades_especiais = models.BooleanField(default=False)
    dt_nascimento = models.DateField('Data Nascimento')
    celular = models.CharField(max_length=11)
    fixo_residencia = models.CharField(max_length=10, blank=True, null=True)
    fixo_trabalho = models.CharField(max_length=10, blank=True, null=True)
    endereco = models.CharField(max_length=120)
    complemento = models.CharField(max_length=120, blank=True, null=True)
    bairro = models.ForeignKey(Bairro, on_delete=models.PROTECT)
    cep = models.CharField(max_length=8, blank=True, null=True)
    escolaridade = models.ForeignKey(Escolaridade, on_delete=models.PROTECT)
    profissao = models.ForeignKey(Profissao, on_delete=models.PROTECT)
    outra_profissao = models.CharField(max_length=50, blank=True, null=True)
    desempregado = models.BooleanField(default=False)
    disponibilidade = models.ManyToManyField(Turno)
    dt_inclusao = models.DateTimeField(auto_now_add=True)
    ordem_judicial = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    cursos = models.ManyToManyField(Curso)

class Horario(models.Model):

    DIA = (
        ('0', ''),
        ('1', 'Domingo'),
        ('2', 'Segunda'),
        ('3', 'Terça'),
        ('4', 'Quarta'),
        ('5', 'Quinta'),
        ('6', 'Sexta'),
        ('7', 'Sábado'),
    )

    class Meta:
        ordering = ('dia_semana','hora_inicio', 'hora_fim')

    def __str__(self):
        return '%s - %s - %s' % (self.dia_semana, self.hora_inicio, self.hora_fim)

    def readable_str(self):
        return '%sª - %s - %s' % (self.DIA[int(self.dia_semana)][0], self.hora_inicio.strftime("%H:%M"), self.hora_fim.strftime("%H:%M"))
#        return '%sª - %s - %s' % (self.DIA[int(self.dia_semana)][0], self.hora_inicio.strftime("%H:%M"), self.hora_fim.strftime("%H:%M"))

    dia_semana = models.CharField(max_length=1, choices=DIA)
    hora_inicio = models.TimeField('Hora Início')
    hora_fim = models.TimeField('Hora Fim')
    dt_inclusao = models.DateTimeField(auto_now_add=True)

class Situacao_Turma(models.Model):
    class Meta:
        verbose_name = "Situação de turma prevista"
        verbose_name_plural = "Situações de turma prevista"

    def __str__(self):
        return self.descricao

    descricao = models.CharField(max_length=10, unique = True, null = True)

class Situacao_Turma_Definitiva(models.Model):
    class Meta:
        verbose_name = "Situação de turma definitiva"
        verbose_name_plural = "Situações de turma definitiva"

    def __str__(self):
        return self.descricao

    descricao = models.CharField(max_length=20, unique = True)

class Turma_Prevista(models.Model):
    class Meta:
        ordering = ('curso', 'nome')
        verbose_name = "Turma Prevista"
        verbose_name_plural = "Turmas Previstas"

    def __str__(self):
        return '%s - %s - %s' % (self.curso, self.nome, self.curriculo)

    nome = models.CharField(max_length=20, unique=True, blank=True, null=True)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    curriculo = models.ForeignKey(Curriculo, on_delete=models.PROTECT)
    instrutor = models.ForeignKey(Instrutor, on_delete=models.PROTECT, blank=True, null=True)
    dt_inicio = models.DateField('Data Início')
    dt_fim = models.DateField('Data Fim', blank=True, null=True)
    horario = models.ManyToManyField(Horario)
    quant_alunos = models.PositiveSmallIntegerField(default=0)
    dt_inclusao = models.DateTimeField(auto_now_add=True)
    exibir = models.BooleanField(default=True)
    situacao = models.ForeignKey(Situacao_Turma, on_delete=models.PROTECT, default=1)

class Turma(models.Model):
    class Meta:
        ordering = ('curso','nome')

    def __str__(self):
        return '%s - %s - %s' % (self.curso, self.nome, self.curriculo)

    nome = models.CharField(max_length=20, unique=True, blank=True, null=True)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    curriculo = models.ForeignKey(Curriculo, on_delete=models.PROTECT)
    instrutor = models.ForeignKey(Instrutor, on_delete=models.PROTECT, blank=True, null=True)
    dt_inicio = models.DateField('Data Início')
    dt_fim = models.DateField('Data Fim')
    horario = models.ManyToManyField(Horario)
    quant_alunos = models.PositiveSmallIntegerField(default=0)
    dt_fechamento = models.DateTimeField('Data Fechamento', blank=True, null=True)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

class Situacao(models.Model):
    class Meta:
        verbose_name = "Situação"
        verbose_name_plural = "Situações"

    def __str__(self):
        return self.descricao

    descricao = models.CharField(max_length=30, unique = True, null = True)

class Aluno_Turma(models.Model):
    class Meta:
        verbose_name_plural = "Relação de Alunos por Turma"
        ordering = ('turma', 'aluno',)

    def __str__(self):
        return '%s - %s' % (self.turma, self.aluno)

    turma = models.ForeignKey(Turma, on_delete=models.PROTECT)
    aluno = models.ForeignKey(Aluno, on_delete=models.PROTECT)
    situacao = models.ForeignKey(Situacao, on_delete=models.PROTECT, default=1)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

class Presenca(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.PROTECT)
    aluno = models.ForeignKey(Aluno, on_delete=models.PROTECT)
    data_aula = models.DateField('Data da Aula', blank=True, null=True)
    presente = models.BooleanField(blank=True, default=False)

class Feriado(models.Model):
    class Meta:
        verbose_name = "Feriado"
        verbose_name_plural = "Feriados"
    nome = models.CharField(max_length = 50, unique = False)
    data = models.DateField()
    fixo = models.BooleanField('Feriado fixo', blank = True, null = True, default=True)

class Status_Aluno_Turma_Prevista(models.Model):
    class Meta:
        verbose_name_plural = "Status de Alunos por Turma Prevista"
        ordering = ('descricao',)

    def __str__(self):
        return self.descricao

    descricao = models.CharField(max_length=60, unique=True)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

class Aluno_Turma_Prevista(models.Model):
    class Meta:
        verbose_name_plural = "Relação de Alunos por Turma - Previsão"
        ordering = ('turma_prevista', 'aluno',)

    def __str__(self):
        return '%s - %s' % (self.turma_prevista, self.aluno)

    turma_prevista = models.ForeignKey(Turma_Prevista, on_delete=models.PROTECT)
    aluno = models.ForeignKey(Aluno, on_delete=models.PROTECT)
    status_aluno_turma_prevista = models.ForeignKey(Status_Aluno_Turma_Prevista, default=1, on_delete=models.PROTECT)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

class Turma_Prevista_Turma_Definitiva(models.Model):
    class Meta:
        verbose_name_plural = "Relação entre turma Prevista e Turma Definitiva"
        ordering = ('turma_prevista', 'turma',)

    def __str__(self):
        return '%s - %s' % (self.turma_prevista, self.turma)

    turma_prevista = models.ForeignKey(Turma_Prevista, on_delete=models.PROTECT)
    turma = models.ForeignKey(Turma, on_delete=models.PROTECT)
    dt_inclusao = models.DateTimeField(auto_now_add=True)
