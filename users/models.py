from django.db import models


class User(models.Model):
    """Пользователь сервиса (своя модель предметной области)."""

    name = models.CharField('имя', max_length=150)
    email = models.EmailField('e-mail', unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.name
