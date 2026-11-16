from django.contrib import admin
from django.db.models import Count

from places.models import Place
from visits.models import Visit


class VisitInline(admin.TabularInline):
    model = Visit
    extra = 0
    fields = ('date', 'user', 'people', 'status', 'rating')
    autocomplete_fields = ('user',)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'capacity', 'hours',
                    'visits_count')
    list_filter = ('category',)
    search_fields = ('name', 'address')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    list_per_page = 20
    inlines = (VisitInline,)
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'category', 'address')}),
        ('Условия посещения', {'fields': ('price', 'capacity',
                                          'open_hour', 'close_hour')}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            visits_total=Count('visits'))

    @admin.display(description='часы работы')
    def hours(self, obj):
        return obj.hours

    @admin.display(description='посещений', ordering='visits_total')
    def visits_count(self, obj):
        return obj.visits_total
