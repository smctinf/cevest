# Generated by Django 2.0.9 on 2018-12-27 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cevest', '0005_auto_20181226_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turma',
            name='nome',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='turma_prevista',
            name='nome',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
