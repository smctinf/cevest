# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Curso(models.Model):
    def __str__(self):
        return self.nome

    nome = models.CharField(max_length=60)
    dt_inclusao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

class Instrutor(models.Model):
    class Meta:
        verbose_name_plural = "Instrutores"

    def __str__(self):
        return self.nome

    nome = models.CharField(max_length=60)
    dt_inclusao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

class Cidade(models.Model):
    def __str__(self):
        return self.nome

    nome = models.CharField(max_length=30)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

class Bairro(models.Model):
    def __str__(self):
        return '%s - %s' % (self.cidade, self.nome)
#        return self.nome

    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    nome = models.CharField(max_length=30)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

class Turno(models.Model):
    def __str__(self):
        return self.nome

    nome = models.CharField(max_length=30)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

class Profissao(models.Model):
    class Meta:
        verbose_name_plural = "Profissões"

    def __str__(self):
        return self.nome

    nome = models.CharField(max_length=50)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

class Escolaridade(models.Model):
    def __str__(self):
        return self.descricao

    descricao = models.CharField(max_length=50)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

SEXO = (
    ('F', 'Feminino'),
    ('M', 'Masculino'),
)

TURNO = (
    ('1', 'Manhã'),
    ('2', 'Tarde'),
    ('4', 'Noite'),
)

class Aluno(models.Model):
    def __str__(self):
        return self.nome

    nome = models.CharField(max_length=60)
    email = models.EmailField(max_length=254, blank=True, null=True)
    cpf = models.CharField(unique=True, max_length=11)
    sexo = models.CharField(max_length=1, choices=SEXO)
    dt_nascimento = models.DateField('Data Nascimento')
    celular = models.CharField(max_length=11)
    fixo_residencia = models.CharField(max_length=10, blank=True, null=True)
    fixo_trabalho = models.CharField(max_length=10, blank=True, null=True)
    endereco = models.CharField(max_length=120)
    bairro = models.ForeignKey(Bairro, on_delete=models.PROTECT)
    escolaridade = models.ForeignKey(Escolaridade, on_delete=models.PROTECT)
    profissao = models.ForeignKey(Profissao, on_delete=models.PROTECT)
    disponibilidade = models.CharField(max_length=1, choices=TURNO)
    dt_inclusao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    cursos = models.ManyToManyField(Curso)
"""
class Aluno_Quer_Curso(models.Model):
#    def __str__(self):
#        return self.nome

    aluno = models.ForeignKey(Aluno, on_delete=models.PROTECT)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    dt_inclusao = models.DateTimeField(auto_now_add=True)
"""