from django import forms

from visits.models import Visit
from visits.validators import validate_not_past


class VisitForm(forms.ModelForm):
    """Создание и редактирование посещения."""

    class Meta:
        model = Visit
        fields = ('place', 'user', 'date', 'people')
        widgets = {
            'place': forms.Select(attrs={'class': 'form-select'}),
            'user': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'type': 'date',
                                           'class': 'form-control'},
                                    format='%Y-%m-%d'),
            'people': forms.NumberInput(attrs={'class': 'form-control',
                                               'min': 1}),
        }
        help_texts = {'people': 'Сколько человек пойдёт, включая вас.'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['place'].empty_label = 'Выберите место'
        self.fields['user'].empty_label = 'Выберите пользователя'

    def clean_date(self):
        day = self.cleaned_data['date']
        validate_not_past(day)
        return day

    def clean(self):
        """Проверяет, что на дату в месте хватает свободной вместимости.
        Отменённые посещения и само редактируемое посещение не учитываются."""
        cleaned = super().clean()
        place, day = cleaned.get('place'), cleaned.get('date')
        people = cleaned.get('people')
        if place and day and people:
            booked = sum(Visit.objects.active()
                         .filter(place=place, date=day)
                         .exclude(pk=self.instance.pk)
                         .values_list('people', flat=True))
            free = place.capacity - booked
            if people > free:
                raise forms.ValidationError(
                    f'В месте «{place}» на {day:%d.%m.%Y} не хватает '
                    f'вместимости: свободно мест — {max(free, 0)}.')
        return cleaned
