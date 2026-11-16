from datetime import date

from django.db.models import Avg, Count, Max, Min, Q, Sum
from django.shortcuts import get_object_or_404, render

from homepage.pagination import paginate
from places.models import Place
from users.models import User
from visits.models import Visit

SORT_OPTIONS = {
    'date': 'Дата ↑',
    '-date': 'Дата ↓',
    '-people': 'Больше людей',
    'place__name': 'Место А–Я',
}


def visit_list(request):
    visits = Visit.objects.select_related('place', 'user')
    status = request.GET.get('status', '')
    if status in dict(Visit.STATUS_CHOICES):
        visits = visits.filter(status=status)
    else:
        status = ''
    day = request.GET.get('date', '')
    try:
        if day:
            visits = visits.filter(date=date.fromisoformat(day))
    except ValueError:
        day = ''
    place = request.GET.get('place', '')
    if place.isdigit():
        visits = visits.filter(place_id=int(place))
    user = request.GET.get('user', '')
    if user.isdigit():
        visits = visits.filter(user_id=int(user))
    sort = request.GET.get('sort', 'date')
    if sort not in SORT_OPTIONS:
        sort = 'date'
    page_obj, querystring = paginate(request, visits.order_by(sort, 'id'), 5)
    context = {
        'page_obj': page_obj,
        'querystring': querystring,
        'status_choices': [('', 'Все')] + Visit.STATUS_CHOICES,
        'sort_options': SORT_OPTIONS,
        'places': Place.objects.only('id', 'name'),
        'users': User.objects.only('id', 'name'),
        'status': status, 'day': day, 'place': place, 'user': user,
        'sort': sort,
    }
    return render(request, 'visits/visit_list.html', context)


def visit_detail(request, visit_id):
    visit = get_object_or_404(
        Visit.objects.select_related('place', 'user'), pk=visit_id)
    return render(request, 'visits/visit_detail.html', {'visit': visit})


def stats(request):
    not_cancelled = ~Q(visits__status=Visit.CANCELLED)
    labels = dict(Visit.STATUS_CHOICES)
    context = {
        'totals': Visit.objects.aggregate(
            visits=Count('id'), people=Sum('people'),
            avg_rating=Avg('rating'), first=Min('date'), last=Max('date')),
        'places_count': Place.objects.count(),
        'by_status': [
            {**row, 'label': labels[row['status']]}
            for row in Visit.objects.values('status')
            .annotate(cnt=Count('id'), people=Sum('people'))
            .order_by('-cnt')],
        'by_place': (Place.objects.annotate(
            cnt=Count('visits'), people=Sum('visits__people'))
            .order_by('-cnt', 'name')),
        'ratings': (Place.objects.filter(visits__rating__isnull=False)
                    .annotate(rating=Avg('visits__rating'),
                              marks=Count('visits__rating'))
                    .order_by('-rating')),
        'popular': (Place.objects.annotate(
            cnt=Count('visits', filter=not_cancelled))
            .filter(cnt__gt=1).order_by('-cnt')),
    }
    return render(request, 'visits/stats.html', context)
