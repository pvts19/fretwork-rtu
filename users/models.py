from django.db import models


class User(models.Model):
    """Пользователь сервиса (своя модель предметной области)."""

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
