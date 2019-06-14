# Generated by Django 2.0.9 on 2018-12-27 00:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cevest', '0007_auto_20181226_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='turma',
            name='instrutor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cevest.Instrutor'),
        ),
        migrations.AddField(
            model_name='turma_prevista',
            name='instrutor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cevest.Instrutor'),
        ),
    ]
