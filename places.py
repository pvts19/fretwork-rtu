"""Функции работы с местами отдыха."""

SORT_KEYS = ("name", "price", "capacity")


def next_id(items: list[dict]) -> int:
    """Возвращает следующий свободный идентификатор."""
    return max((item["id"] for item in items), default=0) + 1


def add_place(places: list[dict], name: str, category: str, address: str,
              price: float, capacity: int,
              open_hour: int, close_hour: int) -> dict:
    """Добавляет новое место в список и возвращает его."""
    if not name.strip():
        raise ValueError("Название не может быть пустым")
    if price < 0 or capacity <= 0:
        raise ValueError("Цена должна быть >= 0, вместимость > 0")
    if not (0 <= open_hour <= 24 and 0 <= close_hour <= 24):
        raise ValueError("Часы работы должны быть от 0 до 24")
    place = {
        "id": next_id(places),
        "name": name.strip(),
        "category": category.strip(),
        "address": address.strip(),
        "price": price,
        "capacity": capacity,
        "open_hour": open_hour,
        "close_hour": close_hour,
    }
    places.append(place)
    return place


def find_place(places: list[dict], place_id: int) -> dict | None:
    """Ищет место по идентификатору."""
    for place in places:
        if place["id"] == place_id:
            return place
    return None


def search_places(places: list[dict], text: str) -> list[dict]:
    """Поиск по подстроке в названии или адресе (без учёта регистра)."""
    text = text.lower()
    return [p for p in places
            if text in p["name"].lower() or text in p["address"].lower()]


def filter_by_category(places: list[dict], category: str) -> list[dict]:
    """Отбирает места заданной категории."""
    return [p for p in places if p["category"].lower() == category.lower()]


def visit_cost(place: dict, people: int) -> float:
    """Стоимость посещения места для компании из people человек."""
    return place["price"] * people


def filter_by_budget(places: list[dict], budget: float,
                     people: int) -> list[dict]:
    """Отбирает места, посещение которых укладывается в бюджет."""
    return [p for p in places if visit_cost(p, people) <= budget]


def sort_places(places: list[dict], key: str = "name",
                reverse: bool = False) -> list[dict]:
    """Сортирует места по названию, цене или вместимости."""
    if key not in SORT_KEYS:
        raise ValueError(f"Сортировка возможна только по: {SORT_KEYS}")
    return sorted(places, key=lambda p: p[key], reverse=reverse)


def is_open_at(place: dict, hour: int) -> bool:
    """Проверяет, открыто ли место в указанный час."""
    start, end = place["open_hour"], place["close_hour"]
    if start <= end:
        return start <= hour < end
    return hour >= start or hour < end  # работает через полночь


def categories(places: list[dict]) -> set[str]:
    """Множество всех категорий мест."""
    return {p["category"] for p in places}
