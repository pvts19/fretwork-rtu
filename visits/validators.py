from datetime import date

from django.core.exceptions import ValidationError


def validate_not_past(value: date) -> None:
    """Запрещает выбирать дату в прошлом."""
    if value < date.today():
        raise ValidationError('Нельзя запланировать посещение на прошедшую '
                              'дату.')
