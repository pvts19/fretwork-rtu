from django.http import Http404
from django.shortcuts import render

from db import queries as q
from db.database import fetch_all, fetch_one

STATUS_CHOICES = [('', 'Все'), ('active', 'Активные'),
                  ('done', 'Завершённые'), ('cancelled', 'Отменённые')]


def visit_list(request):
    status = request.GET.get('status', '')
    if status not in dict(STATUS_CHOICES):
        status = ''
    context = {
        'visits': fetch_all(q.VISIT_LIST, {'status': status}),
        'status': status,
        'status_choices': STATUS_CHOICES,
    }
    return render(request, 'visits/visit_list.html', context)


def visit_detail(request, visit_id):
    visit = fetch_one(q.VISIT_DETAIL, {'id': visit_id})
    if visit is None:
        raise Http404('Посещение не найдено')
    return render(request, 'visits/visit_detail.html', {'visit': visit})


def stats(request):
    context = {
        'totals': fetch_one(q.TOTALS),
        'by_status': fetch_all(q.VISITS_BY_STATUS),
        'by_place': fetch_all(q.VISITS_BY_PLACE),
        'ratings': fetch_all(q.PLACE_RATINGS),
        'popular': fetch_all(q.POPULAR_PLACES, {'min_count': 1}),
    }
    return render(request, 'visits/stats.html', context)
