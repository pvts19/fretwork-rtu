from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from places.models import Place
from users.models import User


class Visit(models.Model):
    """Запланированный поход пользователя в место отдыха."""

    ACTIVE = 'active'
    CANCELLED = 'cancelled'
    DONE = 'done'
    STATUS_CHOICES = [
        (ACTIVE, 'Активно'),
        (CANCELLED, 'Отменено'),
        (DONE, 'Завершено'),
    ]

    place = models.ForeignKey(Place, on_delete=models.CASCADE,
                              related_name='visits')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='visits')
    date = models.DateField()
    people = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default=ACTIVE)
    rating = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        ordering = ['date', 'id']

    def __str__(self):
        return f'№{self.pk} {self.place} — {self.date}'

    @property
    def cost(self):
        return self.place.price * self.people

    def cancel(self):
        """Отменяет активное посещение."""
        if self.status != self.ACTIVE:
            raise ValueError('Отменить можно только активное посещение')
        self.status = self.CANCELLED
        self.save(update_fields=['status'])
