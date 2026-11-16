"""Функции работы с посещениями (запланированными походами в места)."""
from datetime import date

from places import find_place, next_id

ACTIVE = "active"
CANCELLED = "cancelled"
DONE = "done"


def people_on_date(visits: list[dict], place_id: int, day: str,
                   exclude_id: int | None = None) -> int:
    """Сколько человек уже записано в место на дату (активные визиты)."""
    return sum(v["people"] for v in visits
               if v["place_id"] == place_id and v["date"] == day
               and v["status"] == ACTIVE and v["id"] != exclude_id)


def free_capacity(place: dict, visits: list[dict], day: str) -> int:
    """Свободная вместимость места на дату."""
    return place["capacity"] - people_on_date(visits, place["id"], day)


def available_places(places: list[dict], visits: list[dict], day: str,
                     people: int) -> list[dict]:
    """Места, в которых на дату есть место для people человек."""
    return [p for p in places if free_capacity(p, visits, day) >= people]


def create_visit(visits: list[dict], places: list[dict], place_id: int,
                 user_id: int, day: str, people: int) -> dict:
    """Создаёт посещение, проверив дату и свободную вместимость."""
    place = find_place(places, place_id)
    if place is None:
        raise ValueError(f"Место с id={place_id} не найдено")
    if people <= 0:
        raise ValueError("Количество человек должно быть больше 0")
    if date.fromisoformat(day) < date.today():
        raise ValueError("Нельзя запланировать посещение на прошедшую дату")
    if free_capacity(place, visits, day) < people:
        raise ValueError("На эту дату в месте недостаточно свободных мест")
    visit = {
        "id": next_id(visits),
        "place_id": place_id,
        "user_id": user_id,
        "date": day,
        "people": people,
        "status": ACTIVE,
        "rating": None,
    }
    visits.append(visit)
    return visit


def cancel_visit(visits: list[dict], visit_id: int) -> dict:
    """Отменяет активное посещение."""
    for visit in visits:
        if visit["id"] == visit_id:
            if visit["status"] != ACTIVE:
                raise ValueError("Отменить можно только активное посещение")
            visit["status"] = CANCELLED
            return visit
    raise ValueError(f"Посещение с id={visit_id} не найдено")


def place_rating(visits: list[dict], place_id: int) -> float | None:
    """Средняя оценка места по завершённым посещениям."""
    marks = [v["rating"] for v in visits
             if v["place_id"] == place_id and v["rating"] is not None]
    if not marks:
        return None
    return round(sum(marks) / len(marks), 1)


def user_visits(visits: list[dict], user_id: int) -> list[dict]:
    """Все посещения пользователя, отсортированные по дате."""
    return sorted((v for v in visits if v["user_id"] == user_id),
                  key=lambda v: v["date"])
