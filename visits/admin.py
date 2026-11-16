from django.contrib import admin

from visits.models import Visit


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'place', 'user', 'people', 'status',
                    'rating')
    list_display_links = ('id', 'date')
    list_editable = ('status',)
    list_filter = ('status', 'date', 'place__category', 'place')
    search_fields = ('place__name', 'user__name', 'user__email')
    list_select_related = ('place', 'user')
    autocomplete_fields = ('place', 'user')
    date_hierarchy = 'date'
    ordering = ('-date',)
    list_per_page = 20
    actions = ('cancel_selected',)

    @admin.action(description='Отменить выбранные активные посещения')
    def cancel_selected(self, request, queryset):
        updated = queryset.active().update(status=Visit.Status.CANCELLED)
        self.message_user(request, f'Отменено посещений: {updated}')
