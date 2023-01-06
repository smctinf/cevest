# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from .functions import validate_CPF

# Create your models here.


class Pre_requisito(models.Model):

    descricao = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Pré-requisito"
        verbose_name_plural = "Pré-requisitos"
        ordering = ('descricao',)


class Escolaridade(models.Model):

    descricao = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.descricao

    class Meta:
        ordering = ('descricao',)


# Pelo oque deu para entender olhandos as outras models é que a tabela "Curriculo" guarda o período em que os cursos
# estariam sendo executados. Porém, só existe um único currículo, que começou no ano de 2018 e não tem um dt_fim. Então, é facil
# dizer que esse model Curriculo é inútil da maneira que está sendo utilizado no momento, é interessante começarmos a criar novos
# Curriculos ou mesmo deletar essa tabela por completo

class Curriculo(models.Model):

    nome = models.CharField(max_length=30)
    dt_inicio = models.DateField('Data Início')
    dt_fim = models.DateField('Data Fim', blank=True, null=True)
    dt_inclusao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ('dt_inicio', 'dt_fim')

# Esse turno aqui guarda somente três valores: Manhã, Tarde e Noite.
class Turno(models.Model):
    def __str__(self):
        return self.descricao

    descricao = models.CharField(max_length=50)
    dt_inclusao = models.DateTimeField(auto_now_add=True)


# Esse programa é meio que um wrapper para os cursos, ou seja, o tema
# Esse programa aqui é uma foreign key da model Curso, facilitando a filtragem e relacionamento
# de cursos da mesma área
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
    descricao = models.TextField(max_length=2000, verbose_name="Descrição")
    programa = models.ForeignKey(Programa, on_delete=models.PROTECT)
    duracao = models.PositiveSmallIntegerField(default=0, verbose_name="Duração")
    idade_minima = models.PositiveSmallIntegerField(default=0, verbose_name="Idade mínima")
    turnos = models.ManyToManyField(Turno)
    # Sim, escolaridade nesse caso é algo quantitatvo, ainda não explorei a views onde o curso é salvo mas aparentemente
    # utilizam o id para descobrir o valor da escolaridade (1 por exemplo pode ser "ensino fundamental incompleto" e 5 "ensino superior completo")
    escolaridade_minima = models.ForeignKey(
        Escolaridade, on_delete=models.PROTECT, default=1, verbose_name="Escolaridade mínima")
    pre_requisitos = models.ManyToManyField(Pre_requisito, blank=True, verbose_name="Pré-requisitos")
    quant_alunos = models.PositiveSmallIntegerField(default=0, verbose_name="Quantidade máxima de alunos")
    dt_inclusao = models.DateTimeField(auto_now_add=True)
    exibir = models.BooleanField(default=True)
    ativo = models.BooleanField(default=True)


class Disciplina(models.Model):
    def __str__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)

    nome = models.CharField(max_length=100)
    carga_horaria = models.PositiveSmallIntegerField(default=0)


# Pelo o que compreendi, as Matrizes armazenam a quantidade de aulas e carga horária total de uma determinada disciplina em um curso
# Meio grandinha eesa explicação mas acontece do seguinte jeito:
# O CURSO "Oficina de Mesa Posta" tem em seu currículo a disciplina "Laço para guardanapo", e é a partir das matrizes que a quantidade de aulas e a carga horária
# são armazenadas

class Matriz(models.Model):
    class Meta:
        verbose_name_plural = "Matrizes"

    def __int__(self):
        return '%s - %s - %s' % (self.curriculo, self.curso, self.disciplina)

    curriculo = models.ForeignKey(
        Curriculo, on_delete=models.PROTECT, default=True)
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

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    nome = models.CharField(max_length=60)
    matricula = models.CharField(unique=True, null=True, max_length=11)
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


# Colocar Profissão como um model tem suas vantagens e desvantagens
# A principal vantagem é a pesquisa rápida de alunos de determinada profissão e a coleta de dados, que é importante para esse projeto "cidade inteligente"
# que friburgo almeja alcançar
# Porém, não é muito fácil fazer uma lista de todas as profissões existentes no mundo kkkkkkk, então no formulário deve existir um campo "outro" ou "outra profissão"
# para cadastrar essa possível profissão que ainda não existe. Precisar ser verificado se as views já fazem isso

class Profissao(models.Model):
    class Meta:
        verbose_name_plural = "Profissões"
        ordering = ('nome',)

    def __str__(self):
        return self.nome

    nome = models.CharField(max_length=50)
    dt_inclusao = models.DateTimeField(auto_now_add=True)





class Aluno(models.Model):

    # O ideal era criar um ChoiceField com uma opção do usuário escrever no campo "outro"
    SEXO_CHOICES = (
        ('F', 'Feminino'),
        ('M', 'Masculino'),
        ('N', 'Não binário/Não declarado'),
        ('O', 'Outro'),
    )

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)

    nome = models.CharField(max_length=128)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    dt_nascimento = models.DateField('Data de nascimento')
    escolaridade = models.ForeignKey(Escolaridade, on_delete=models.PROTECT)
    profissao = models.ForeignKey(Profissao, on_delete=models.PROTECT)

    # ACHEI! DEFINITIVAMENTE esse campo não deveria existir. Ao cadastrar uma profissão no outro era para ela ser cadastrada e já ser inserida na profissão
    outra_profissao = models.CharField(max_length=50, blank=True, null=True)
    desempregado = models.BooleanField(default=False)

    email = models.EmailField(max_length=254, blank=True, null=True)
    cpf = models.CharField(unique=True, max_length=11,
                           validators=[validate_CPF])
    celular = models.CharField(max_length=11)
    fixo_residencia = models.CharField(max_length=10, blank=True, null=True)
    fixo_trabalho = models.CharField(max_length=10, blank=True, null=True)
    endereco = models.CharField(max_length=120)
    complemento = models.CharField(max_length=120, blank=True, null=True)
    bairro = models.ForeignKey(Bairro, on_delete=models.PROTECT)
    cep = models.CharField(max_length=8, blank=True, null=True)

    nis = models.CharField(unique=True, max_length=11, blank=True, null=True)
    bolsa_familia = models.BooleanField(default=False)
    quant_filhos = models.PositiveSmallIntegerField(default=0)
    portador_necessidades_especiais = models.BooleanField(default=False)

    disponibilidade = models.ManyToManyField(Turno)
    dt_inclusao = models.DateTimeField(auto_now_add=True)
    ordem_judicial = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)

    cpf_file = models.FileField(upload_to='cpf_file', verbose_name='CPF', null=True)
    identidade_file = models.FileField(
        upload_to='identidade_file', verbose_name='Identidade', null=True)
    comprovante_residencia_file = models.FileField(
        upload_to='comprovante_residencia_file', verbose_name='Comproante de residência', null=True)


    # Essa aqui também parece ser uma péssima ideia. Como o curso não é algo que a pessoa está necessariamente (O aluno faz parte de uma turma para ser mais exato),
    # seria mais sábio criar um ManyToManyField com uma relação entre Aluno e Turma, tipo no sistema de cursos livres
    cursos = models.ManyToManyField(Curso)


class Horario(models.Model):

    # descobri pq tem esse, aparentemente o python considera 0 como segunda. Enfim, o loyola tem uma função no app Administração para fazer ess conversão
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
        ordering = ('dia_semana', 'hora_inicio', 'hora_fim')

    def __str__(self):
        return '%s - %s - %s' % (self.dia_semana, self.hora_inicio, self.hora_fim)

    def readable_str(self):
        return '%sª - %s - %s' % (self.DIA[int(self.dia_semana)][0], self.hora_inicio.strftime("%H:%M"), self.hora_fim.strftime("%H:%M"))

    dia_semana = models.CharField(max_length=1, choices=DIA)
    hora_inicio = models.TimeField('Hora Início')
    hora_fim = models.TimeField('Hora Fim')
    dt_inclusao = models.DateTimeField(auto_now_add=True)


# Essa coisa de situação de turma é algo a ser estuado, pq aparentemente tem situações diferentes para turmas normais e "definitivas" (que ainda não sei o que são)
class Situacao_Turma(models.Model):
    class Meta:
        verbose_name = "Situação de turma prevista"
        verbose_name_plural = "Situações de turma prevista"

    def __str__(self):
        return self.descricao

    descricao = models.CharField(max_length=32, unique=True)


class Situacao_Turma_Definitiva(models.Model):
    class Meta:
        verbose_name = "Situação de turma definitiva"
        verbose_name_plural = "Situações de turma definitiva"

    def __str__(self):
        return self.descricao

    descricao = models.CharField(max_length=32, unique=True)
    dt_inclusao = models.DateTimeField(auto_now_add=True)


# Aqui que começa meu problema, não existe apenas um model Turma, e sim diversas formas de turma que, na minha opinião, não precisavam existir.
# Muito provavelmente o melhor seja criar um campo "status" para a turma que descreva se ela é uma turma ainda em planejamento (ou seja, "prevista"), ou uma
# tuma ativa, ou finalizada e assim por diante
class Turma_Prevista(models.Model):
    class Meta:
        ordering = ('curso', 'nome')
        verbose_name = "Turma Prevista"
        verbose_name_plural = "Turmas Previstas"

    def __str__(self):
        return '%s - %s - %s' % (self.curso, self.nome, self.curriculo)

    # Esse campo nome aqui é um pouco enganoso. O nome, aparentemente, é na realidade que a turma recebe baseado no curso, data de início e turno
    # Tenho que descobrir se esse nome é inserido pelo usuário ou tem alguma lógica no backend que já está atribuindo esses nomes
    nome = models.CharField(max_length=20, unique=True, blank=True, null=True)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    curriculo = models.ForeignKey(Curriculo, on_delete=models.PROTECT)
    instrutor = models.ForeignKey(
        Instrutor, on_delete=models.PROTECT, blank=True, null=True)
    dt_inicio = models.DateField('Data Início')
    dt_fim = models.DateField('Data Fim', blank=True, null=True)
    horario = models.ManyToManyField(Horario)
    quant_alunos = models.PositiveSmallIntegerField(default=0)
    dt_inclusao = models.DateTimeField(auto_now_add=True)
    turno = models.ForeignKey(Turno, on_delete=models.PROTECT, null=True)
    exibir = models.BooleanField(default=True)
    situacao = models.ForeignKey(
        Situacao_Turma, on_delete=models.PROTECT, default=1)


# Esse Turma aqui tem alguns campos a mais que o Turma_Prevista, e são eles: Turno e dt_fechamento. Como eu disse no comentário da
# Turma_Prevista, podemos muito bem utilizar somente um model.
class Turma(models.Model):
    class Meta:
        ordering = ('curso', 'nome')

    def __str__(self):
        return '%s - %s - %s' % (self.curso, self.nome, self.curriculo)

    nome = models.CharField(max_length=20, unique=True)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    curriculo = models.ForeignKey(Curriculo, on_delete=models.PROTECT)
    instrutor = models.ForeignKey(
        Instrutor, on_delete=models.PROTECT)
    dt_inicio = models.DateField('Data Início')
    dt_fim = models.DateField('Data Fim')
    turno = models.ForeignKey(Turno, on_delete=models.PROTECT, null=True)
    horario = models.ManyToManyField(Horario)
    quant_alunos = models.PositiveSmallIntegerField(default=0)
    dt_fechamento = models.DateTimeField(
        'Data Fechamento', blank=True, null=True)
    exibir = models.BooleanField(default=True)
    situacao = models.ForeignKey(
        Situacao_Turma, on_delete=models.PROTECT, default=1)
    dt_inclusao = models.DateTimeField(auto_now_add=True)


class Situacao(models.Model):
    class Meta:
        verbose_name = "Situação"
        verbose_name_plural = "Situações"

    def __str__(self):
        return self.descricao

    descricao = models.CharField(max_length=32, unique=True)


# Bem, aqui que está a relação de Turma e Aluno. Não me importo de não 
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

# Essa relação aqui parece ok, só penso que poderia haver uma tabela "aula" que poderia segurar essas informações
class Presenca(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.PROTECT)
    aluno = models.ForeignKey(Aluno, on_delete=models.PROTECT)
    data_aula = models.DateField('Data da Aula', blank=True, null=True)
    presente = models.BooleanField(blank=True, default=False)

# Essa tabela aqui tem que ser investigado, descobrir onde isso é usado
class Feriado(models.Model):
    class Meta:
        verbose_name = "Feriado"
        verbose_name_plural = "Feriados"
    nome = models.CharField(max_length=50, unique=False)
    data = models.DateField()
    fixo = models.BooleanField(
        'Feriado fixo', blank=True, null=True, default=True)

# Outra daquele negócio destatus exclusivo para turma prevista, mas essa aqui é só para ALUNO
class Status_Aluno_Turma_Prevista(models.Model):
    class Meta:
        verbose_name_plural = "Status de Alunos por Turma Prevista"
        ordering = ('descricao',)

    def __str__(self):
        return self.descricao

    descricao = models.CharField(max_length=60, unique=True)
    dt_inclusao = models.DateTimeField(auto_now_add=True)


# Mesma coisa, ver a necessidade da existência de uma tabela dessas. Mas essa até que é uma relação dahora
class Aluno_Turma_Prevista(models.Model):
    class Meta:
        verbose_name_plural = "Relação de Alunos por Turma - Previsão"
        ordering = ('turma_prevista', 'aluno',)
        unique_together = ['turma_prevista', 'aluno']

    def __str__(self):
        return '%s - %s' % (self.turma_prevista, self.aluno)

    turma_prevista = models.ForeignKey(
        Turma_Prevista, on_delete=models.PROTECT)
    aluno = models.ForeignKey(Aluno, on_delete=models.PROTECT)
    status_aluno_turma_prevista = models.ForeignKey(
        Status_Aluno_Turma_Prevista, default=1, on_delete=models.PROTECT)
    dt_inclusao = models.DateTimeField(auto_now_add=True)


# Bem, isso aqui n faz muito sentido kkkkkkkk, pq vc teria uma relação de um com outro. Enfim, outra coisa para ser estudada
class Turma_Prevista_Turma_Definitiva(models.Model):
    class Meta:
        verbose_name_plural = "Relação entre turma Prevista e Turma Definitiva"
        ordering = ('turma_prevista', 'turma',)

    def __str__(self):
        return '%s - %s' % (self.turma_prevista, self.turma)

    turma_prevista = models.ForeignKey(
        Turma_Prevista, on_delete=models.PROTECT)
    turma = models.ForeignKey(Turma, on_delete=models.PROTECT)
    dt_inclusao = models.DateTimeField(auto_now_add=True)
