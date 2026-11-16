from django.http import Http404
from django.shortcuts import render

from place_service import find_place
from storage import load_places, load_users, load_visits


def visit_list(request):
    places = load_places()
    users = {u.id: u for u in load_users()}
    rows = [{'visit': v, 'place': find_place(places, v.place_id),
             'user': users.get(v.user_id)}
            for v in sorted(load_visits(), key=lambda v: v.date)]
    return render(request, 'visits/visit_list.html', {'rows': rows})


def visit_detail(request, visit_id):
    visit = next((v for v in load_visits() if v.id == visit_id), None)
    if visit is None:
        raise Http404('Посещение не найдено')
    place = find_place(load_places(), visit.place_id)
    user = next((u for u in load_users() if u.id == visit.user_id), None)
    context = {
        'visit': visit,
        'place': place,
        'user': user,
        'cost': place.cost(visit.people) if place else None,
    }
    return render(request, 'visits/visit_detail.html', context)
