from django.db import migrations, models

from places.translit import make_slug


def fill_slugs(apps, schema_editor):
    Place = apps.get_model('places', 'Place')
    used = set()
    for place in Place.objects.order_by('id'):
        base = make_slug(place.name) or 'place'
        slug, n = base, 2
        while slug in used:
            slug, n = f'{base}-{n}', n + 1
        used.add(slug)
        place.slug = slug
        place.save(update_fields=['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=160),
            preserve_default=False,
        ),
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='place',
            name='slug',
            field=models.SlugField(blank=True, max_length=160, unique=True,
                                   verbose_name='слаг (адрес страницы)'),
        ),
    ]
