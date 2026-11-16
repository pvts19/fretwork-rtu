from django.shortcuts import render

from place_service import categories
from storage import load_places, load_visits


def index(request):
    places = load_places()
    context = {
        'places_count': len(places),
        'active_count': sum(v.is_active for v in load_visits()),
        'categories': sorted(categories(places)),
    }
    return render(request, 'homepage/index.html', context)
