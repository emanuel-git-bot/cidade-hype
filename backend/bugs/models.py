from django.db import models

class BugReport(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('resolved', 'Resolvido'),
    ]

    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição')
    screenshot = models.ImageField('Captura de Tela', upload_to='bugs/', blank=True, null=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    resolved_at = models.DateTimeField('Data de Resolução', null=True, blank=True)
    resolution_notes = models.TextField('Notas da Resolução', blank=True)

    class Meta:
        verbose_name = 'Bug Reportado'
        verbose_name_plural = 'Bugs Reportados'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def resolve(self, notes=''):
        from django.utils import timezone
        self.status = 'resolved'
        self.resolved_at = timezone.now()
        self.resolution_notes = notes
        self.save() 