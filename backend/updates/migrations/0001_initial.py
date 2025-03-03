# Generated by Django 5.1.5 on 2025-01-26 05:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ComingSoon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
            ],
            options={
                'verbose_name': 'Em Breve',
                'verbose_name_plural': 'Em Breve',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
            ],
            options={
                'verbose_name': 'Atualização',
                'verbose_name_plural': 'Atualizações',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ComingSoonImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='coming_soon/', verbose_name='Imagem')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('coming_soon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='updates.comingsoon', verbose_name='Em Breve')),
            ],
            options={
                'verbose_name': 'Imagem do Em Breve',
                'verbose_name_plural': 'Imagens do Em Breve',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='UpdateImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='updates/', verbose_name='Imagem')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('update', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='updates.update', verbose_name='Atualização')),
            ],
            options={
                'verbose_name': 'Imagem da Atualização',
                'verbose_name_plural': 'Imagens da Atualização',
                'ordering': ['created_at'],
            },
        ),
    ]
