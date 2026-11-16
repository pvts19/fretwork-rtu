from django.http import Http404
from django.shortcuts import render

from place_service import find_place, sort_places
from storage import load_places, load_visits
from visit_service import place_rating


def place_list(request):
    context = {'places': sort_places(load_places(), 'name')}
    return render(request, 'places/place_list.html', context)


def place_detail(request, place_id):
    place = find_place(load_places(), place_id)
    if place is None:
        raise Http404('Место не найдено')
    visits = load_visits()
    context = {
        'place': place,
        'rating': place_rating(visits, place.id),
        'visits': sorted((v for v in visits
                          if v.place_id == place.id and v.is_active),
                         key=lambda v: v.date),
    }
    return render(request, 'places/place_detail.html', context)
