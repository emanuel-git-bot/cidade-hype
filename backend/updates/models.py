from django.db import models

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
    update = models.ForeignKey(Update, on_delete=models.CASCADE, related_name='images', verbose_name='Atualização')
    image = models.ImageField('Imagem', upload_to='updates/')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Imagem da Atualização'
        verbose_name_plural = 'Imagens da Atualização'
        ordering = ['created_at']

    def __str__(self):
        return f'Imagem {self.id} - {self.update.title}'

class ComingSoon(models.Model):
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Em Breve'
        verbose_name_plural = 'Em Breve'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class ComingSoonImage(models.Model):
    coming_soon = models.ForeignKey(ComingSoon, on_delete=models.CASCADE, related_name='images', verbose_name='Em Breve')
    image = models.ImageField('Imagem', upload_to='coming_soon/')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Imagem do Em Breve'
        verbose_name_plural = 'Imagens do Em Breve'
        ordering = ['created_at']

    def __str__(self):
        return f'Imagem {self.id} - {self.coming_soon.title}' 