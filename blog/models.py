from django.conf import settings
from django.db import models

from base.models import NULLABLE


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name='Владелец',
                             **NULLABLE)

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержимое статьи')
    image = models.ImageField(verbose_name='Изображение', upload_to='image/%Y', **NULLABLE)
    count_views = models.IntegerField(verbose_name='Колличство просмотров', default=0)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
