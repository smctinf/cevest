# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from .functions import validate_CPF

# Create your models here.

class Pre_requisito(models.Model):
    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Pré-Requisito"
#        verbose_name_plural = "Matrizes"
        ordering = ('descricao',)

    descricao = models.CharField(max_length=100)
#    atende = models.BooleanField(default=False)

class Escolaridade(models.Model):
    def __str__(self):
        return self.descricao

    class Meta:
        ordering = ('descricao',)

    descricao = models.CharField(max_length=50)
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

class Curso(models.Model):
    def __str__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)

    nome = models.CharField(max_length=60)
    descricao = models.TextField(max_length=2000)
    duracao = models.PositiveSmallIntegerField()
    idade_minima = models.PositiveSmallIntegerField()
    escolaridade_minima = models.ForeignKey(Escolaridade, on_delete=models.PROTECT)
    pre_requisito = models.ManyToManyField(Pre_requisito, blank=True)
    quant_alunos = models.PositiveSmallIntegerField(default=0)
    dt_inclusao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

class Disciplina(models.Model):
    def __str__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)

    nome = models.CharField(max_length=60)
    carga_horaria = models.PositiveSmallIntegerField()

class Matriz(models.Model):
    class Meta:
        verbose_name_plural = "Matrizes"

    def __int__(self):
        return '%s - %s - %s' % (self.curriculo, self.curso, self.disciplina)

    curriculo = models.ForeignKey(Curriculo, on_delete=models.PROTECT, default=True)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT)
    num_aulas = models.PositiveSmallIntegerField()

class Instrutor(models.Model):
    class Meta:
        verbose_name_plural = "Instrutores"
        ordering = ('nome',)

    def __str__(self):
        return self.nome

    nome = models.CharField(max_length=60)
    dt_inclusao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

class Cidade(models.Model):
    def __str__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)

    nome = models.CharField(max_length=30)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

class Bairro(models.Model):
    def __str__(self):
        return '%s - %s' % (self.cidade, self.nome)
#        return self.nome

    class Meta:
        ordering = ('cidade', 'nome',)

    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    nome = models.CharField(max_length=30)
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
#    cpf = models.CharField(unique=True, max_length=11)
    cpf = models.CharField(unique=True, max_length=11, validators=[validate_CPF])

    nis = models.IntegerField(unique=True, blank=True, null=True)
    bolsa_familia = models.BooleanField(default=False)
    quant_filhos = models.PositiveSmallIntegerField(default=0)
    sexo = models.CharField(max_length=1, choices=SEXO)
    portador_necessidades_especiais = models.BooleanField(default=False)
    dt_nascimento = models.DateField('Data Nascimento')
    celular = models.CharField(max_length=11)
    fixo_residencia = models.CharField(max_length=10, blank=True, null=True)
    fixo_trabalho = models.CharField(max_length=10, blank=True, null=True)
    endereco = models.CharField(max_length=120)
    bairro = models.ForeignKey(Bairro, on_delete=models.PROTECT)
    escolaridade = models.ForeignKey(Escolaridade, on_delete=models.PROTECT)
    profissao = models.ForeignKey(Profissao, on_delete=models.PROTECT)
    desempregado = models.BooleanField(default=False)
    disponibilidade = models.ManyToManyField(Turno)
    dt_inclusao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    cursos = models.ManyToManyField(Curso)

class Horario(models.Model):

    DIA = (
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

    dia_semana = models.CharField(max_length=1, choices=DIA)
    hora_inicio = models.TimeField('Hora Início')
    hora_fim = models.TimeField('Hora Fim')
    dt_inclusao = models.DateTimeField(auto_now_add=True)

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

class Turma(models.Model):
    class Meta:
        ordering = ('curso',)

    def __str__(self):
        return '%s - %s - %s' % (self.nome, self.curso, self.curriculo)

    nome = models.CharField(max_length=20, unique=True, blank=True, null=True)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    curriculo = models.ForeignKey(Curriculo, on_delete=models.PROTECT)
    instrutor = models.ForeignKey(Instrutor, on_delete=models.PROTECT, blank=True, null=True)
    dt_inicio = models.DateField('Data Início')
    dt_fim = models.DateField('Data Fim', blank=True, null=True)
    horario = models.ManyToManyField(Horario)
    quant_alunos = models.PositiveSmallIntegerField(default=0)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

class Aluno_Turma(models.Model):
    class Meta:
        ordering = ('turma', 'aluno',)

    def __str__(self):
        return '%s - %s' % (self.turma, self.aluno)

    turma = models.ForeignKey(Turma, on_delete=models.PROTECT)
    aluno = models.ForeignKey(Aluno, on_delete=models.PROTECT)
    dt_inclusao = models.DateTimeField(auto_now_add=True)
