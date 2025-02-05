from django.db import models

class BugReport(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('resolved', 'Resolvido'),
    )

    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição')
    screenshot = models.ImageField('Captura de Tela', upload_to='bug_reports/', null=True, blank=True)
    user_id = models.CharField('ID do Roblox', max_length=50)
    username = models.CharField('Nome de usuário', max_length=100)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    resolved_at = models.DateTimeField('Resolvido em', null=True, blank=True)
    resolution_notes = models.TextField('Notas da Resolução', blank=True)

    class Meta:
        verbose_name = 'Bug Reportado'
        verbose_name_plural = 'Bugs Reportados'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.username}'

    def mark_as_resolved(self, notes=''):
        from django.utils import timezone
        self.status = 'resolved'
        self.resolved_at = timezone.now()
        self.resolution_notes = notes
        self.save()

class RobloxUser(models.Model):
    user_id = models.CharField('ID do Roblox', max_length=50, unique=True)
    username = models.CharField('Nome de usuário', max_length=100)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    last_login = models.DateTimeField('Último login', null=True, blank=True)

    class Meta:
        verbose_name = 'Usuário do Roblox'
        verbose_name_plural = 'Usuários do Roblox'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.username} ({self.user_id})'

    def update_last_login(self):
        from django.utils import timezone
        self.last_login = timezone.now()
        self.save() 