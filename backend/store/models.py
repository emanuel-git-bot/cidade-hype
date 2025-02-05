from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Slug', unique=True)
    icon = models.CharField('Ícone', max_length=50, help_text='Nome do ícone do Font Awesome')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items', verbose_name='Categoria')
    name = models.CharField('Nome', max_length=200)
    description = models.TextField('Descrição')
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    image = models.ImageField('Imagem', upload_to='items/')
    observation = models.TextField('Observação', blank=True, help_text='Detalhes sobre o que será entregue ao jogador')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('paid', 'Pago'),
        ('delivered', 'Entregue'),
        ('cancelled', 'Cancelado'),
    )

    user_id = models.CharField('ID do Roblox', max_length=50)
    username = models.CharField('Nome de usuário', max_length=100)
    item = models.ForeignKey(Item, on_delete=models.PROTECT, verbose_name='Item')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_id = models.CharField('ID do Pagamento', max_length=100, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    delivered_at = models.DateTimeField('Entregue em', null=True, blank=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']

    def __str__(self):
        return f'Pedido {self.id} - {self.username}'

    def mark_as_delivered(self):
        self.status = 'delivered'
        self.delivered_at = timezone.now()
        self.save()

class Bug(models.Model):
    STATUS_CHOICES = (
        ('open', 'Aberto'),
        ('in_progress', 'Em Andamento'),
        ('resolved', 'Resolvido'),
        ('closed', 'Fechado'),
    )

    PRIORITY_CHOICES = (
        ('low', 'Baixa'),
        ('medium', 'Média'),
        ('high', 'Alta'),
        ('critical', 'Crítica'),
    )

    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição')
    steps = models.TextField('Passos para Reproduzir')
    user_id = models.CharField('ID do Roblox', max_length=50)
    username = models.CharField('Nome de usuário', max_length=100)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField('Prioridade', max_length=20, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    resolved_at = models.DateTimeField('Resolvido em', null=True, blank=True)
    resolution_notes = models.TextField('Notas de Resolução', blank=True)

    class Meta:
        verbose_name = 'Bug'
        verbose_name_plural = 'Bugs'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def mark_as_resolved(self, notes=''):
        self.status = 'resolved'
        self.resolved_at = timezone.now()
        self.resolution_notes = notes
        self.save()

class Update(models.Model):
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Atualização'
        verbose_name_plural = 'Atualizações'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class UpdateImage(models.Model):
    update = models.ForeignKey(Update, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Imagem', upload_to='updates/')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Imagem da Atualização'
        verbose_name_plural = 'Imagens das Atualizações'
        ordering = ['created_at']

class UpdateLink(models.Model):
    update = models.ForeignKey(Update, on_delete=models.CASCADE, related_name='links')
    title = models.CharField('Título', max_length=100)
    url = models.URLField('URL')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Link da Atualização'
        verbose_name_plural = 'Links das Atualizações'
        ordering = ['created_at']

class Event(models.Model):
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição')
    date = models.DateTimeField('Data do Evento')
    location = models.CharField('Local', max_length=200)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-date']

    def __str__(self):
        return self.title

class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Imagem', upload_to='events/')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Imagem do Evento'
        verbose_name_plural = 'Imagens dos Eventos'
        ordering = ['created_at']

class ComingSoon(models.Model):
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição')
    release_date = models.DateField('Data de Lançamento', null=True, blank=True)
    status = models.CharField('Status', max_length=50, default='Em Desenvolvimento')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Em Breve'
        verbose_name_plural = 'Em Breve'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class ComingSoonImage(models.Model):
    coming_soon = models.ForeignKey(ComingSoon, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Imagem', upload_to='coming_soon/')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Imagem do Em Breve'
        verbose_name_plural = 'Imagens do Em Breve'
        ordering = ['created_at'] 