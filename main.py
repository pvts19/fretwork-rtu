"""RestSpot — сервис поиска мест для отдыха. Начальный сценарий (ПР1).

Сценарий: пользователь вводит бюджет и количество человек, программа
сообщает, подходит ли ему место, открыто ли оно сейчас и как оно оценено.
"""
from datetime import datetime

# Данные одного места отдыха (коллекции и классы появятся в ПР2–ПР3)
place_name = "Парк Горького"
place_category = "Парк"
place_address = "Москва, ул. Крымский Вал, 9"
price_per_person = 350.0
open_hour = 8
close_hour = 23
rating = 4.7


def calc_visit_cost(price, people):
    """Возвращает стоимость посещения для компании из people человек."""
    return round(price * people, 2)


def is_within_budget(cost, budget):
    """Проверяет, укладывается ли стоимость в бюджет."""
    return cost <= budget


def is_open_now(open_from, open_to, hour):
    """Проверяет, открыто ли место в указанный час."""
    if open_from <= open_to:
        return open_from <= hour < open_to
    # Место работает через полночь, например с 20 до 4
    return hour >= open_from or hour < open_to


def rating_to_text(value):
    """Переводит числовой рейтинг (0–5) в текстовую оценку."""
    if value >= 4.5:
        return "отлично"
    elif value >= 3.5:
        return "хорошо"
    elif value >= 2.5:
        return "средне"
    return "плохо"


def main():
    print("=== RestSpot: поиск мест для отдыха ===")
    print(f"Место: {place_name} ({place_category})")
    print(f"Адрес: {place_address}")
    print(f"Рейтинг: {rating} — {rating_to_text(rating)}")

    budget_input = input("Ваш бюджет, руб.: ").strip()
    people_input = input("Сколько человек: ").strip()

    if not people_input.isdigit() or int(people_input) == 0:
        print("Ошибка: количество человек должно быть целым числом больше 0")
        return
    try:
        budget = float(budget_input.replace(",", "."))
    except ValueError:
        print("Ошибка: бюджет должен быть числом")
        return
    people = int(people_input)

    cost = calc_visit_cost(price_per_person, people)
    print(f"Стоимость посещения на {people} чел.: {cost} руб.")

    if is_within_budget(cost, budget):
        print(f"Укладывается в бюджет, останется {budget - cost} руб.")
    else:
        print(f"Не хватает {cost - budget} руб.")

    hour = datetime.now().hour
    if is_open_now(open_hour, close_hour, hour):
        print(f"Сейчас {hour} ч — место открыто до {close_hour}:00")
    else:
        print(f"Сейчас {hour} ч — место закрыто, откроется в {open_hour}:00")


if __name__ == "__main__":
    main()
