"""Тесты форм ПР11: создание, редактирование, отмена, валидация, загрузка."""
import shutil
from datetime import date, timedelta
from io import BytesIO

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image

from places.forms import PlaceForm
from places.models import Place
from users.models import User
from visits.forms import VisitForm
from visits.models import Visit

DAY = date.today() + timedelta(days=7)


@pytest.fixture
def cafe(db):
    return Place.objects.create(name='Кафе', category='Кафе', address='ул. А',
                                price=500, capacity=10, open_hour=10,
                                close_hour=22)


@pytest.fixture
def user(db):
    return User.objects.create(name='Анна', email='anna@example.com')


def visit_data(cafe, user, **extra):
    return {'place': cafe.pk, 'user': user.pk, 'date': DAY.isoformat(),
            'people': 4, **extra}


def test_create_visit(client, cafe, user):
    response = client.post(reverse('visits:create'), visit_data(cafe, user))
    visit = Visit.objects.get()
    assert response.status_code == 302
    assert response.url == visit.get_absolute_url()
    assert visit.status == Visit.Status.ACTIVE


def test_past_date_rejected(cafe, user):
    past = (date.today() - timedelta(days=1)).isoformat()
    form = VisitForm(visit_data(cafe, user, date=past))
    assert not form.is_valid() and 'date' in form.errors


def test_capacity_check_ignores_cancelled(cafe, user):
    Visit.objects.create(place=cafe, user=user, date=DAY, people=8)
    Visit.objects.create(place=cafe, user=user, date=DAY, people=8,
                         status=Visit.Status.CANCELLED)
    assert not VisitForm(visit_data(cafe, user, people=3)).is_valid()
    assert VisitForm(visit_data(cafe, user, people=2)).is_valid()


def test_edit_does_not_conflict_with_itself(client, cafe, user):
    visit = Visit.objects.create(place=cafe, user=user, date=DAY, people=10)
    response = client.post(reverse('visits:edit', args=[visit.pk]),
                           visit_data(cafe, user, people=9))
    assert response.status_code == 302
    visit.refresh_from_db()
    assert visit.people == 9


def test_edit_missing_visit_404(client, db):
    assert client.get(reverse('visits:edit', args=[999])).status_code == 404


def test_cancel_requires_post(client, cafe, user):
    visit = Visit.objects.create(place=cafe, user=user, date=DAY, people=2)
    url = reverse('visits:cancel', args=[visit.pk])
    assert client.get(url).status_code == 405
    client.post(url)
    visit.refresh_from_db()
    assert visit.status == Visit.Status.CANCELLED
    # отменённое посещение не блокирует место
    assert VisitForm(visit_data(cafe, user, people=10)).is_valid()


def test_csrf_token_in_forms(client, cafe):
    html = client.get(reverse('visits:create')).content.decode()
    assert 'csrfmiddlewaretoken' in html


def test_place_form_validation(db):
    form = PlaceForm({'name': ' Парк ', 'category': 'Парк', 'address': 'ул.',
                      'price': 0, 'capacity': 0, 'open_hour': 8,
                      'close_hour': 8})
    assert not form.is_valid()
    assert 'capacity' in form.errors and 'close_hour' in form.errors


@pytest.fixture
def media_root(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    yield tmp_path
    shutil.rmtree(tmp_path, ignore_errors=True)


def test_create_place_with_image(client, db, media_root):
    buffer = BytesIO()
    Image.new('RGB', (10, 10), 'green').save(buffer, 'PNG')
    image = SimpleUploadedFile('park.png', buffer.getvalue(), 'image/png')
    response = client.post(reverse('places:create'), {
        'name': 'Новый парк', 'category': 'Парк', 'address': 'ул. Б',
        'description': 'Тенистые аллеи', 'price': 0, 'capacity': 50,
        'open_hour': 6, 'close_hour': 23, 'image': image})
    place = Place.objects.get(name='Новый парк')
    assert response.status_code == 302
    assert place.slug == 'novyy-park' and place.image.name
    page = client.get(place.get_absolute_url()).content.decode()
    assert place.image.url in page


def test_search_form_invalid_price_ignored(client, cafe):
    response = client.get(reverse('places:list'), {'max_price': '-5'})
    assert response.status_code == 200
    assert response.context['form'].errors


def test_detail_title_is_clean(client, cafe, user):
    visit = Visit.objects.create(place=cafe, user=user, date=DAY, people=2)
    html = client.get(visit.get_absolute_url()).content.decode()
    title = html.split('<title>')[1].split('</title>')[0]
    assert '<' not in title
