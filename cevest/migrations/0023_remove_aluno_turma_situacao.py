# Generated by Django 2.1.7 on 2019-04-10 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cevest', '0022_auto_20190410_1126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aluno_turma',
            name='situacao',
        ),
    ]
