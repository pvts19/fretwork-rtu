from datetime import date

from django.http import Http404
from django.shortcuts import render

from db import queries as q
from db.database import fetch_all, fetch_one


def place_list(request):
    category = request.GET.get('category', '')
    text = request.GET.get('q', '').strip()
    if text:
        places = fetch_all(q.PLACES_SEARCH, {'text': f'%{text}%'})
    elif category:
        places = fetch_all(q.PLACES_BY_CATEGORY, {'category': category})
    else:
        places = fetch_all(q.PLACE_LIST)
    context = {
        'places': places,
        'categories': [r['category'] for r in fetch_all(q.CATEGORIES)],
        'category': category,
        'text': text,
    }
    return render(request, 'places/place_list.html', context)


def place_detail(request, place_id):
    place = fetch_one(q.PLACE_BY_ID, {'id': place_id})
    if place is None:
        raise Http404('Место не найдено')
    context = {
        'place': place,
        'rating': fetch_one(q.PLACE_RATING, {'id': place_id})['rating'],
        'visits': fetch_all(q.PLACE_ACTIVE_VISITS, {'id': place_id}),
    }
    return render(request, 'places/place_detail.html', context)


def free_places(request):
    """Поиск мест со свободной вместимостью на выбранную дату."""
    day = request.GET.get('date', '')
    people = request.GET.get('people', '1')
    context = {'day': day, 'people': people, 'places': None, 'error': ''}
    if day:
        try:
            date.fromisoformat(day)
            people_count = int(people)
            if people_count < 1:
                raise ValueError
        except ValueError:
            context['error'] = 'Укажите корректную дату и число человек ≥ 1'
        else:
            context['places'] = fetch_all(
                q.FREE_PLACES, {'date': day, 'people': people_count})
    return render(request, 'places/free_places.html', context)
