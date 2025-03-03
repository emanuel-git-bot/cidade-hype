# Generated by Django 5.1.5 on 2025-01-26 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BugReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('screenshot', models.ImageField(blank=True, null=True, upload_to='bugs/', verbose_name='Captura de Tela')),
                ('status', models.CharField(choices=[('pending', 'Pendente'), ('resolved', 'Resolvido')], default='pending', max_length=20, verbose_name='Status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('resolved_at', models.DateTimeField(blank=True, null=True, verbose_name='Data de Resolução')),
                ('resolution_notes', models.TextField(blank=True, verbose_name='Notas da Resolução')),
            ],
            options={
                'verbose_name': 'Bug Reportado',
                'verbose_name_plural': 'Bugs Reportados',
                'ordering': ['-created_at'],
            },
        ),
    ]
