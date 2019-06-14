# Generated by Django 2.0.9 on 2018-12-18 22:18

import cevest.functions
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('cpf', models.CharField(max_length=11, unique=True, validators=[cevest.functions.validate_CPF])),
                ('nis', models.IntegerField(blank=True, null=True, unique=True)),
                ('bolsa_familia', models.BooleanField(default=False)),
                ('quant_filhos', models.PositiveSmallIntegerField(default=0)),
                ('sexo', models.CharField(choices=[('F', 'Feminino'), ('M', 'Masculino')], max_length=1)),
                ('portador_necessidades_especiais', models.BooleanField(default=False)),
                ('dt_nascimento', models.DateField(verbose_name='Data Nascimento')),
                ('celular', models.CharField(max_length=11)),
                ('fixo_residencia', models.CharField(blank=True, max_length=10, null=True)),
                ('fixo_trabalho', models.CharField(blank=True, max_length=10, null=True)),
                ('endereco', models.CharField(max_length=120)),
                ('desempregado', models.BooleanField(default=False)),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True)),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('nome',),
            },
        ),
        migrations.CreateModel(
            name='Aluno_Turma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cevest.Aluno')),
            ],
            options={
                'ordering': ('turma', 'aluno'),
            },
        ),
        migrations.CreateModel(
            name='Bairro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('cidade', 'nome'),
            },
        ),
        migrations.CreateModel(
            name='Cidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('nome',),
            },
        ),
        migrations.CreateModel(
            name='Curriculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('dt_inicio', models.DateField(verbose_name='Data Início')),
                ('dt_fim', models.DateField(blank=True, null=True, verbose_name='Data Fim')),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('dt_fim', 'nome'),
            },
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60)),
                ('descricao', models.TextField(max_length=2000)),
                ('duracao', models.PositiveSmallIntegerField()),
                ('idade_minima', models.PositiveSmallIntegerField()),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True)),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('nome',),
            },
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60)),
                ('carga_horaria', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ('nome',),
            },
        ),
        migrations.CreateModel(
            name='Escolaridade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50)),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('descricao',),
            },
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_semana', models.CharField(choices=[('1', 'Domingo'), ('2', 'Segunda'), ('3', 'Terça'), ('4', 'Quarta'), ('5', 'Quinta'), ('6', 'Sexta'), ('7', 'Sábado')], max_length=1)),
                ('hora_inicio', models.TimeField(verbose_name='Hora Início')),
                ('hora_fim', models.TimeField(verbose_name='Hora Fim')),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('turma_prevista',),
            },
        ),
        migrations.CreateModel(
            name='Instrutor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60)),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True)),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Instrutores',
                'ordering': ('nome',),
            },
        ),
        migrations.CreateModel(
            name='Matriz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_aulas', models.PositiveSmallIntegerField()),
                ('curriculo', models.ForeignKey(default=True, on_delete=django.db.models.deletion.PROTECT, to='cevest.Curriculo')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cevest.Curso')),
                ('disciplina', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cevest.Disciplina')),
            ],
            options={
                'verbose_name_plural': 'Matrizes',
            },
        ),
        migrations.CreateModel(
            name='Pre_requisito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Pré-Requisito',
                'ordering': ('descricao',),
            },
        ),
        migrations.CreateModel(
            name='Profissao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Profissões',
                'ordering': ('nome',),
            },
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_inicio', models.DateField(verbose_name='Data Início')),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True)),
                ('curriculo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cevest.Curriculo')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cevest.Curso')),
            ],
            options={
                'ordering': ('curso',),
            },
        ),
        migrations.CreateModel(
            name='Turma_Prevista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_inicio', models.DateField(verbose_name='Data Início')),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True)),
                ('curriculo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cevest.Curriculo')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cevest.Curso')),
            ],
            options={
                'ordering': ('curso',),
            },
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50)),
                ('dt_inclusao', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='horario',
            name='turma_prevista',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cevest.Turma_Prevista'),
        ),
        migrations.AddField(
            model_name='curso',
            name='escolaridade_minima',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cevest.Escolaridade'),
        ),
        migrations.AddField(
            model_name='curso',
            name='pre_requisito',
            field=models.ManyToManyField(to='cevest.Pre_requisito'),
        ),
        migrations.AddField(
            model_name='bairro',
            name='cidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cevest.Cidade'),
        ),
        migrations.AddField(
            model_name='aluno_turma',
            name='turma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cevest.Turma'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='bairro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cevest.Bairro'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='cursos',
            field=models.ManyToManyField(to='cevest.Curso'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='disponibilidade',
            field=models.ManyToManyField(to='cevest.Turno'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='escolaridade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cevest.Escolaridade'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='profissao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cevest.Profissao'),
        ),
    ]
