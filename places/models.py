from django.core.validators import MaxValueValidator
from django.db import models


class Place(models.Model):
    CATEGORY_CHOICES = [
        ('Парк', 'Парк'),
        ('Кафе', 'Кафе'),
        ('Пляж', 'Пляж'),
        ('Музей', 'Музей'),
        ('База отдыха', 'База отдыха'),
        ('Другое', 'Другое'),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    address = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    capacity = models.PositiveIntegerField()
    open_hour = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(24)])
    close_hour = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(24)])

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def hours(self):
        return f'{self.open_hour}:00–{self.close_hour}:00'
