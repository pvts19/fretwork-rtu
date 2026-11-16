from django import forms

from places.models import Place

SORT_CHOICES = [
    ('name', 'По названию'),
    ('price', 'Сначала дешёвые'),
    ('-price', 'Сначала дорогие'),
    ('-rating', 'По рейтингу'),
    ('-visits_count', 'По популярности'),
]


class PlaceSearchForm(forms.Form):
    """Поиск и фильтрация мест (GET-форма, класс Form)."""

    q = forms.CharField(
        label='Поиск', required=False, max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'type': 'search',
            'placeholder': 'Название или адрес'}))
    category = forms.ChoiceField(
        label='Категория', required=False,
        choices=[('', 'Все категории')] + Place.Category.choices,
        widget=forms.Select(attrs={'class': 'form-select'}))
    max_price = forms.DecimalField(
        label='Цена до', required=False, min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'placeholder': 'Цена до'}))
    sort = forms.ChoiceField(
        label='Сортировка', required=False, choices=SORT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}))


class PlaceForm(forms.ModelForm):
    """Добавление и редактирование места, включая загрузку фото."""

    class Meta:
        model = Place
        fields = ('name', 'category', 'address', 'description', 'price',
                  'capacity', 'open_hour', 'close_hour', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control',
                                              'min': 0}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control',
                                                 'min': 1}),
            'open_hour': forms.NumberInput(attrs={'class': 'form-control',
                                                  'min': 0, 'max': 24}),
            'close_hour': forms.NumberInput(attrs={'class': 'form-control',
                                                   'min': 0, 'max': 24}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        return self.cleaned_data['name'].strip()

    def clean_capacity(self):
        capacity = self.cleaned_data['capacity']
        if capacity < 1:
            raise forms.ValidationError('Вместимость должна быть больше 0.')
        return capacity

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('open_hour') == cleaned.get('close_hour') is not None:
            self.add_error('close_hour',
                           'Время закрытия должно отличаться от открытия.')
        return cleaned
