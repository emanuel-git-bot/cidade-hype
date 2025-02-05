from django.db import models

class Event(models.Model):
    STATUS_CHOICES = (
        ('ongoing', 'Em Andamento'),
        ('finished', 'Finalizado'),
    )

    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='ongoing')
    start_date = models.DateTimeField('Data de Início')
    end_date = models.DateTimeField('Data de Término', null=True, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-start_date']

    def __str__(self):
        return self.title

class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images', verbose_name='Evento')
    image = models.ImageField('Imagem', upload_to='events/')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Imagem do Evento'
        verbose_name_plural = 'Imagens do Evento'
        ordering = ['created_at']

    def __str__(self):
        return f'Imagem {self.id} - {self.event.title}'

class EventLink(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='links', verbose_name='Evento')
    title = models.CharField('Título', max_length=100)
    url = models.URLField('URL')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Link do Evento'
        verbose_name_plural = 'Links do Evento'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.title} - {self.event.title}' 