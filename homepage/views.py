from django.shortcuts import render

from db import queries as q
from db.database import fetch_all, fetch_one


def index(request):
    totals = fetch_one(q.TOTALS)
    context = {
        'places_count': totals['places'],
        'active_count': totals['active'] or 0,
        'categories': [r['category'] for r in fetch_all(q.CATEGORIES)],
    }
    return render(request, 'homepage/index.html', context)
