from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse

from places.translit import make_slug


class Place(models.Model):
    class Category(models.TextChoices):
        PARK = 'Парк', 'Парк'
        CAFE = 'Кафе', 'Кафе'
        BEACH = 'Пляж', 'Пляж'
        MUSEUM = 'Музей', 'Музей'
        RESORT = 'База отдыха', 'База отдыха'
        OTHER = 'Другое', 'Другое'

    name = models.CharField('название', max_length=150)
    slug = models.SlugField('слаг (адрес страницы)', max_length=160,
                            unique=True, blank=True)
    category = models.CharField('категория', max_length=50,
                                choices=Category.choices)
    address = models.CharField('адрес', max_length=255)
    price = models.DecimalField('цена на человека, руб.', max_digits=10,
                                decimal_places=2, default=0)
    capacity = models.PositiveIntegerField('вместимость, чел.')
    open_hour = models.PositiveSmallIntegerField(
        'открывается (час)', validators=[MaxValueValidator(24)])
    close_hour = models.PositiveSmallIntegerField(
        'закрывается (час)', validators=[MaxValueValidator(24)])
    description = models.TextField('описание', blank=True)
    image = models.ImageField('фото', upload_to='places/', blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'место отдыха'
        verbose_name_plural = 'места отдыха'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = make_slug(self.name) or 'place'
            slug, n = base, 2
            while Place.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug, n = f'{base}-{n}', n + 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('places:detail', args=[self.slug])

    @property
    def hours(self):
        return f'{self.open_hour}:00–{self.close_hour}:00'
