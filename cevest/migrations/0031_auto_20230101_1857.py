# Generated by Django 3.2.16 on 2023-01-01 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cevest', '0030_auto_20230101_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='turnos',
            field=models.ManyToManyField(to='cevest.Turno'),
        ),
        migrations.AddField(
            model_name='turma',
            name='turno',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='cevest.turno'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='aluno',
            name='comprovante_residencia_file',
            field=models.FileField(upload_to='comprovante_residencia_file', verbose_name='Comproante de residência'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='cpf_file',
            field=models.FileField(upload_to='cpf_file', verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='identidade_file',
            field=models.FileField(upload_to='identidade_file', verbose_name='Identidade'),
        ),
    ]
