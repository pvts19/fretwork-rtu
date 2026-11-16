"""Тесты моделей и ORM-представлений Django."""
from datetime import date, timedelta

import pytest
from django.urls import reverse

from places.models import Place
from users.models import User
from visits.models import Visit

DAY = date.today() + timedelta(days=10)


@pytest.fixture
def data(db):
    cafe = Place.objects.create(name='Кафе', category='Кафе', address='ул. А',
                                price=500, capacity=10, open_hour=10,
                                close_hour=22)
    park = Place.objects.create(name='Парк', category='Парк', address='ул. Б',
                                price=0, capacity=100, open_hour=6,
                                close_hour=24)
    user = User.objects.create(name='Анна', email='anna@example.com')
    Visit.objects.create(place=cafe, user=user, date=DAY, people=8)
    Visit.objects.create(place=cafe, user=user, date=DAY, people=5,
                         status=Visit.CANCELLED)
    Visit.objects.create(place=park, user=user, date=date(2020, 1, 1),
                         people=2, status=Visit.DONE, rating=4)
    return cafe, park, user


def test_related_objects(data):
    cafe, park, user = data
    assert cafe.visits.count() == 2
    assert user.visits.count() == 3
    visit = Visit.objects.select_related('place', 'user').first()
    assert visit.place.name and visit.user.name == 'Анна'


def test_cancel(data):
    visit = Visit.objects.filter(status=Visit.ACTIVE).get()
    visit.cancel()
    assert Visit.objects.get(pk=visit.pk).status == Visit.CANCELLED
    with pytest.raises(ValueError):
        visit.cancel()


def test_free_places_ignore_cancelled(client, data):
    url = reverse('places:free')
    response = client.get(url, {'date': DAY.isoformat(), 'people': 2})
    names = [p.name for p in response.context['places']]
    assert set(names) == {'Кафе', 'Парк'}
    response = client.get(url, {'date': DAY.isoformat(), 'people': 3})
    assert [p.name for p in response.context['places']] == ['Парк']


def test_place_list_search_and_sort(client, data):
    response = client.get(reverse('places:list'), {'q': 'Кафе'})
    assert [p.name for p in response.context['page_obj']] == ['Кафе']
    response = client.get(reverse('places:list'), {'sort': '-price'})
    assert response.context['page_obj'][0].name == 'Кафе'


def test_visit_list_filters(client, data):
    url = reverse('visits:list')
    response = client.get(url, {'status': 'active'})
    assert response.context['page_obj'].paginator.count == 1
    response = client.get(url, {'status': 'oops', 'date': 'bad'})
    assert response.status_code == 200
    assert response.context['page_obj'].paginator.count == 3


def test_missing_objects_404(client, data):
    assert client.get(reverse('places:detail', args=[999])).status_code == 404
    assert client.get(reverse('visits:detail', args=[999])).status_code == 404


def test_stats(client, data):
    response = client.get(reverse('visits:stats'))
    assert response.context['totals']['visits'] == 3
    assert response.status_code == 200
