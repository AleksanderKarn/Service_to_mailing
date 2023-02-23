from django.conf import settings
from django.db import models

from base.models import NULLABLE


class Subscriber(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)
    email = models.EmailField('Емейл адрес')
    full_name = models.CharField('Полное имя', max_length=250)
    comment = models.TextField('Комментарий')

    def __str__(self):
        return f'{self.full_name}, {self.email}, {self.comment}'

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
