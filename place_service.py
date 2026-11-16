"""Функции работы с коллекцией мест отдыха."""
from models import Place

SORT_KEYS = ("name", "price", "capacity")


def next_id(items: list) -> int:
    """Возвращает следующий свободный идентификатор."""
    return max((item.id for item in items), default=0) + 1


def add_place(places: list[Place], name: str, category: str, address: str,
              price: float, capacity: int,
              open_hour: int, close_hour: int) -> Place:
    """Создаёт место (проверки — в конструкторе Place) и добавляет его."""
    place = Place(next_id(places), name, category, address, price, capacity,
                  open_hour, close_hour)
    places.append(place)
    return place


def find_place(places: list[Place], place_id: int) -> Place | None:
    """Ищет место по идентификатору."""
    for place in places:
        if place.id == place_id:
            return place
    return None


def search_places(places: list[Place], text: str) -> list[Place]:
    """Поиск по подстроке в названии или адресе (без учёта регистра)."""
    text = text.lower()
    return [p for p in places
            if text in p.name.lower() or text in p.address.lower()]


def filter_by_category(places: list[Place], category: str) -> list[Place]:
    """Отбирает места заданной категории."""
    return [p for p in places if p.category.lower() == category.lower()]


def filter_by_budget(places: list[Place], budget: float,
                     people: int) -> list[Place]:
    """Отбирает места, посещение которых укладывается в бюджет."""
    return [p for p in places if p.cost(people) <= budget]


def sort_places(places: list[Place], key: str = "name",
                reverse: bool = False) -> list[Place]:
    """Сортирует места по названию, цене или вместимости."""
    if key not in SORT_KEYS:
        raise ValueError(f"Сортировка возможна только по: {SORT_KEYS}")
    return sorted(places, key=lambda p: getattr(p, key), reverse=reverse)


def categories(places: list[Place]) -> set[str]:
    """Множество всех категорий мест."""
    return {p.category for p in places}
