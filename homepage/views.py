from django.db.models import Count, Q
from django.shortcuts import render

from places.models import Place
from visits.models import Visit


def index(request):
    stats = Visit.objects.aggregate(
        active=Count('id', filter=Q(status=Visit.ACTIVE)))
    context = {
        'places_count': Place.objects.count(),
        'active_count': stats['active'],
        'categories': (Place.objects.order_by('category')
                       .values_list('category', flat=True).distinct()),
    }
    return render(request, 'homepage/index.html', context)
