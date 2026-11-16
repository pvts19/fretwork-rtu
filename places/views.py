from datetime import date

from django.contrib import messages
from django.db.models import Avg, Count, Q, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect, render

from homepage.pagination import paginate
from places.forms import PlaceForm, PlaceSearchForm
from places.models import Place
from visits.models import Visit


def place_list(request):
    form = PlaceSearchForm(request.GET or None)
    places = Place.objects.annotate(
        rating=Avg('visits__rating'),
        visits_count=Count('visits', filter=~Q(
            visits__status=Visit.Status.CANCELLED)),
    )
    sort = 'name'
    if form.is_valid():
        data = form.cleaned_data
        if data['q']:
            places = places.filter(Q(name__icontains=data['q'])
                                   | Q(address__icontains=data['q']))
        if data['category']:
            places = places.filter(category=data['category'])
        if data['max_price'] is not None:
            places = places.filter(price__lte=data['max_price'])
        sort = data['sort'] or 'name'
    page_obj, querystring = paginate(request, places.order_by(sort, 'name'))
    context = {'form': form, 'page_obj': page_obj,
               'querystring': querystring}
    return render(request, 'places/place_list.html', context)


def place_detail(request, slug):
    place = get_object_or_404(
        Place.objects.annotate(rating=Avg('visits__rating')), slug=slug)
    context = {
        'place': place,
        'rating': place.rating,
        'visits': place.visits.active().select_related('user'),
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
                visits__date=chosen, visits__status=Visit.Status.ACTIVE)), 0)
            context['places'] = [
                p for p in Place.objects.annotate(booked=booked)
                if p.capacity - p.booked >= people_count]
            for place in context['places']:
                place.free = place.capacity - place.booked
    return render(request, 'places/free_places.html', context)


def place_create(request):
    form = PlaceForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        place = form.save()
        messages.success(request, f'Место «{place}» добавлено.')
        return redirect(place)
    return render(request, 'places/place_form.html', {'form': form})


def place_edit(request, slug):
    place = get_object_or_404(Place, slug=slug)
    form = PlaceForm(request.POST or None, request.FILES or None,
                     instance=place)
    if form.is_valid():
        form.save()
        messages.success(request, 'Изменения сохранены.')
        return redirect(place)
    return render(request, 'places/place_form.html',
                  {'form': form, 'place': place})
