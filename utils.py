"""Ввод и вывод данных в консоли."""
from datetime import date

from models import Place


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


def print_places(places: list[Place], hour: int | None = None) -> None:
    """Печатает список мест; если задан час — отмечает, открыто ли место."""
    if not places:
        print("Ничего не найдено")
    for place in places:
        if hour is None:
            print(place)
        else:
            state = "открыто" if place.is_open_at(hour) else "закрыто"
            print(f"{place} — {state}")
