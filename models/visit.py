"""Посещение — запланированный поход пользователя в место отдыха."""
from datetime import date
from functools import wraps

from models.base import Entity

ACTIVE = "active"
CANCELLED = "cancelled"
DONE = "done"
STATUSES = {ACTIVE: "активно", CANCELLED: "отменено", DONE: "завершено"}


def only_active(method):
    """Декоратор: метод можно вызвать только для активного посещения."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.is_active:
            raise ValueError("Операция доступна только для активного "
                             "посещения")
        return method(self, *args, **kwargs)
    return wrapper


class Visit(Entity):
    """Посещение места: дата, количество человек, статус, оценка."""

    def __init__(self, id: int, place_id: int, user_id: int, date: str,
                 people: int, status: str = ACTIVE,
                 rating: int | None = None) -> None:
        super().__init__(id)
        if people <= 0:
            raise ValueError("Количество человек должно быть больше 0")
        if status not in STATUSES:
            raise ValueError(f"Неизвестный статус: {status}")
        if rating is not None and not 1 <= rating <= 5:
            raise ValueError("Оценка должна быть от 1 до 5")
        self.place_id = place_id
        self.user_id = user_id
        self.date = date
        self.people = people
        self._status = status  # меняется только через методы
        self.rating = rating

    @property
    def status(self) -> str:
        return self._status

    @property
    def is_active(self) -> bool:
        return self._status == ACTIVE

    @only_active
    def cancel(self) -> None:
        """Отменяет посещение."""
        self._status = CANCELLED

    @only_active
    def complete(self, rating: int | None = None) -> None:
        """Отмечает посещение завершённым и сохраняет оценку."""
        if rating is not None and not 1 <= rating <= 5:
            raise ValueError("Оценка должна быть от 1 до 5")
        self._status = DONE
        self.rating = rating

    @property
    def day(self) -> date:
        """Дата посещения как объект date (для шаблонов и сравнений)."""
        return date.fromisoformat(self.date)

    @property
    def status_label(self) -> str:
        return STATUSES[self._status]

    @staticmethod
    def is_past(day: str) -> bool:
        return date.fromisoformat(day) < date.today()

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["status"] = data.pop("_status")
        return data

    def __str__(self) -> str:
        return (f"№{self.id} {self.date}: место {self.place_id}, "
                f"{self.people} чел., {STATUSES[self._status]}")
