# Generated by Django 2.1.7 on 2019-04-17 16:50

import cevest.functions
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cevest', '0027_auto_20190411_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='cpf',
            field=models.CharField(max_length=11, unique=True, validators=[cevest.functions.validate_CPF]),
        ),
        migrations.AlterField(
            model_name='curso',
            name='duracao',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='curso',
            name='escolaridade_minima',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='cevest.Escolaridade'),
        ),
        migrations.AlterField(
            model_name='curso',
            name='idade_minima',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='disciplina',
            name='carga_horaria',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='disciplina',
            name='nome',
            field=models.CharField(max_length=100),
        ),
    ]
