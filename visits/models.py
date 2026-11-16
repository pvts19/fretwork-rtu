from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from places.models import Place
from users.models import User


class VisitQuerySet(models.QuerySet):
    def active(self):
        """Только активные посещения — они занимают вместимость места."""
        return self.filter(status=Visit.Status.ACTIVE)


class Visit(models.Model):
    """Запланированный поход пользователя в место отдыха."""

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Активно'
        CANCELLED = 'cancelled', 'Отменено'
        DONE = 'done', 'Завершено'

    place = models.ForeignKey(Place, on_delete=models.CASCADE,
                              related_name='visits', verbose_name='место')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='visits',
                             verbose_name='пользователь')
    date = models.DateField('дата')
    people = models.PositiveIntegerField(
        'количество человек', validators=[MinValueValidator(1)])
    status = models.CharField('статус', max_length=10,
                              choices=Status.choices, default=Status.ACTIVE)
    rating = models.PositiveSmallIntegerField(
        'оценка', null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)])

    objects = VisitQuerySet.as_manager()

    class Meta:
        ordering = ['date', 'id']
        verbose_name = 'посещение'
        verbose_name_plural = 'посещения'

    def __str__(self):
        return f'№{self.pk} {self.place} — {self.date}'

    def get_absolute_url(self):
        return reverse('visits:detail', args=[self.pk])

    @property
    def cost(self):
        return self.place.price * self.people

    def cancel(self):
        """Отменяет активное посещение."""
        if self.status != self.Status.ACTIVE:
            raise ValueError('Отменить можно только активное посещение')
        self.status = self.Status.CANCELLED
        self.save(update_fields=['status'])
