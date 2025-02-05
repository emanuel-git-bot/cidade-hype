# Generated by Django 5.1.5 on 2025-01-26 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('steps', models.TextField(verbose_name='Passos para Reproduzir')),
                ('user_id', models.CharField(max_length=50, verbose_name='ID do Roblox')),
                ('username', models.CharField(max_length=100, verbose_name='Nome de usuário')),
                ('status', models.CharField(choices=[('open', 'Aberto'), ('in_progress', 'Em Andamento'), ('resolved', 'Resolvido'), ('closed', 'Fechado')], default='open', max_length=20, verbose_name='Status')),
                ('priority', models.CharField(choices=[('low', 'Baixa'), ('medium', 'Média'), ('high', 'Alta'), ('critical', 'Crítica')], default='medium', max_length=20, verbose_name='Prioridade')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('resolved_at', models.DateTimeField(blank=True, null=True, verbose_name='Resolvido em')),
                ('resolution_notes', models.TextField(blank=True, verbose_name='Notas de Resolução')),
            ],
            options={
                'verbose_name': 'Bug',
                'verbose_name_plural': 'Bugs',
                'ordering': ['-created_at'],
            },
        ),
    ]
