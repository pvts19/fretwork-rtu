from datetime import date

from django.db.models import Avg, Count, Q, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, render

from homepage.pagination import paginate
from places.models import Place
from visits.models import Visit

SORT_OPTIONS = {
    'name': 'По названию',
    'price': 'Сначала дешёвые',
    '-price': 'Сначала дорогие',
    '-rating': 'По рейтингу',
    '-visits_count': 'По популярности',
}


def place_list(request):
    places = Place.objects.annotate(
        rating=Avg('visits__rating'),
        visits_count=Count('visits', filter=~Q(
            visits__status=Visit.CANCELLED)),
    )
    text = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')
    max_price = request.GET.get('max_price', '')
    sort = request.GET.get('sort', 'name')
    if text:
        places = places.filter(Q(name__icontains=text)
                               | Q(address__icontains=text))
    if category:
        places = places.filter(category=category)
    if max_price.isdigit():
        places = places.filter(price__lte=int(max_price))
    if sort not in SORT_OPTIONS:
        sort = 'name'
    places = places.order_by(sort, 'name')
    page_obj, querystring = paginate(request, places)
    context = {
        'page_obj': page_obj,
        'querystring': querystring,
        'categories': Place.CATEGORY_CHOICES,
        'sort_options': SORT_OPTIONS,
        'text': text,
        'category': category,
        'max_price': max_price,
        'sort': sort,
    }
    return render(request, 'places/place_list.html', context)


def place_detail(request, place_id):
    place = get_object_or_404(
        Place.objects.annotate(rating=Avg('visits__rating')), pk=place_id)
    context = {
        'place': place,
        'rating': place.rating,
        'visits': (place.visits.filter(status=Visit.ACTIVE)
                   .select_related('user')),
    }
    return render(request, 'places/place_detail.html', context)


def free_places(request):
    """Места со свободной вместимостью на дату (отменённые не учитываются)."""
    day = request.GET.get('date', '')
    people = request.GET.get('people', '1')
    context = {'day': day, 'people': people, 'places': None, 'error': ''}
    if day:
        try:
            chosen = date.fromisoformat(day)
            people_count = int(people)
            if people_count < 1:
                raise ValueError
        except ValueError:
            context['error'] = 'Укажите корректную дату и число человек ≥ 1'
        else:
            booked = Coalesce(Sum('visits__people', filter=Q(
                visits__date=chosen, visits__status=Visit.ACTIVE)), 0)
            context['places'] = [
                p for p in Place.objects.annotate(booked=booked)
                if p.capacity - p.booked >= people_count]
            for place in context['places']:
                place.free = place.capacity - place.booked
    return render(request, 'places/free_places.html', context)
