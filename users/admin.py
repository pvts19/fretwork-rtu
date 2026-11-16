from django.contrib import admin

from users.models import User
from visits.models import Visit


class VisitInline(admin.TabularInline):
    model = Visit
    extra = 0
    fields = ('date', 'place', 'people', 'status', 'rating')
    autocomplete_fields = ('place',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')
    ordering = ('name',)
    list_per_page = 20
    inlines = (VisitInline,)
