"""Ввод и вывод данных в консоли."""
from datetime import date

from places import is_open_at


def ask_int(prompt: str, minimum: int = 0) -> int:
    """Запрашивает целое число, пока не будет введено корректное."""
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
        except ValueError:
            print("Введите целое число")
            continue
        if number < minimum:
            print(f"Число должно быть не меньше {minimum}")
            continue
        return number


def ask_float(prompt: str) -> float:
    """Запрашивает неотрицательное число."""
    while True:
        try:
            number = float(input(prompt).strip().replace(",", "."))
        except ValueError:
            print("Введите число")
            continue
        if number < 0:
            print("Число не может быть отрицательным")
            continue
        return number


def ask_date(prompt: str) -> str:
    """Запрашивает дату в формате ГГГГ-ММ-ДД."""
    while True:
        value = input(prompt).strip()
        try:
            date.fromisoformat(value)
        except ValueError:
            print("Формат даты: ГГГГ-ММ-ДД, например 2026-12-31")
            continue
        return value


def format_place(place: dict, hour: int | None = None) -> str:
    """Строка с описанием места."""
    text = (f"[{place['id']}] {place['name']} ({place['category']}) — "
            f"{place['address']}, {place['price']} руб./чел., "
            f"до {place['capacity']} чел., "
            f"{place['open_hour']}:00–{place['close_hour']}:00")
    if hour is not None:
        text += " — открыто" if is_open_at(place, hour) else " — закрыто"
    return text


def print_places(places: list[dict], hour: int | None = None) -> None:
    """Печатает список мест."""
    if not places:
        print("Ничего не найдено")
    for place in places:
        print(format_place(place, hour))
