# Generated by Django 2.0.9 on 2018-12-27 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cevest', '0008_auto_20181226_2236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='horario',
            name='turma_prevista',
        ),
        migrations.AddField(
            model_name='turma',
            name='horario',
            field=models.ManyToManyField(to='cevest.Horario'),
        ),
        migrations.AddField(
            model_name='turma_prevista',
            name='horario',
            field=models.ManyToManyField(to='cevest.Horario'),
        ),
    ]
