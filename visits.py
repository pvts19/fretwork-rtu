"""Функции работы с коллекцией посещений."""
from models import Place, Visit
from places import find_place, next_id


def available_places(places: list[Place], visits: list[Visit], day: str,
                     people: int) -> list[Place]:
    """Места, в которых на дату есть место для people человек."""
    return [p for p in places if p.free_capacity(visits, day) >= people]


def create_visit(visits: list[Visit], places: list[Place], place_id: int,
                 user_id: int, day: str, people: int) -> Visit:
    """Создаёт посещение, проверив дату и свободную вместимость."""
    place = find_place(places, place_id)
    if place is None:
        raise ValueError(f"Место с id={place_id} не найдено")
    if Visit.is_past(day):
        raise ValueError("Нельзя запланировать посещение на прошедшую дату")
    if place.free_capacity(visits, day) < people:
        raise ValueError("На эту дату в месте недостаточно свободных мест")
    visit = Visit(next_id(visits), place_id, user_id, day, people)
    visits.append(visit)
    return visit


def find_visit(visits: list[Visit], visit_id: int) -> Visit:
    for visit in visits:
        if visit.id == visit_id:
            return visit
    raise ValueError(f"Посещение с id={visit_id} не найдено")


def cancel_visit(visits: list[Visit], visit_id: int) -> Visit:
    """Отменяет активное посещение."""
    visit = find_visit(visits, visit_id)
    visit.cancel()
    return visit


def place_rating(visits: list[Visit], place_id: int) -> float | None:
    """Средняя оценка места по посещениям с оценкой."""
    marks = [v.rating for v in visits
             if v.place_id == place_id and v.rating is not None]
    if not marks:
        return None
    return round(sum(marks) / len(marks), 1)
