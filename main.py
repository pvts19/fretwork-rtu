"""RestSpot — сервис поиска мест для отдыха. Консольная версия (ПР2)."""
from datetime import datetime

import places as pl
import visits as vs
from storage import (PLACES_FILE, USERS_FILE, VISITS_FILE, load_json,
                     save_json)
from utils import ask_date, ask_float, ask_int, print_places

MENU = """
=== RestSpot: поиск мест для отдыха ===
1. Показать все места
2. Поиск по названию или адресу
3. Места по категории
4. Места по бюджету
5. Сортировка мест
6. Свободные места на дату
7. Запланировать посещение
8. Отменить посещение
9. Мои посещения
10. Добавить место
0. Выход"""


def main() -> None:
    try:
        places = load_json(PLACES_FILE)
        users = load_json(USERS_FILE)
        visits = load_json(VISITS_FILE)
    except ValueError as error:
        print(f"Ошибка загрузки данных: {error}")
        return

    while True:
        print(MENU)
        choice = input("Выберите пункт: ").strip()
        try:
            if choice == "0":
                break
            elif choice == "1":
                print_places(places, datetime.now().hour)
            elif choice == "2":
                print_places(pl.search_places(places, input("Текст: ")))
            elif choice == "3":
                print("Категории:", ", ".join(sorted(pl.categories(places))))
                print_places(pl.filter_by_category(places,
                                                   input("Категория: ")))
            elif choice == "4":
                budget = ask_float("Бюджет, руб.: ")
                people = ask_int("Сколько человек: ", 1)
                print_places(pl.filter_by_budget(places, budget, people))
            elif choice == "5":
                key = input(f"Поле сортировки {pl.SORT_KEYS}: ").strip()
                print_places(pl.sort_places(places, key))
            elif choice == "6":
                day = ask_date("Дата (ГГГГ-ММ-ДД): ")
                people = ask_int("Сколько человек: ", 1)
                print_places(vs.available_places(places, visits, day, people))
            elif choice == "7":
                visit = vs.create_visit(
                    visits, places,
                    place_id=ask_int("id места: ", 1),
                    user_id=ask_int("id пользователя: ", 1),
                    day=ask_date("Дата (ГГГГ-ММ-ДД): "),
                    people=ask_int("Сколько человек: ", 1),
                )
                save_json(VISITS_FILE, visits)
                print(f"Посещение №{visit['id']} запланировано")
            elif choice == "8":
                vs.cancel_visit(visits, ask_int("id посещения: ", 1))
                save_json(VISITS_FILE, visits)
                print("Посещение отменено")
            elif choice == "9":
                for u in users:
                    print(f"[{u['id']}] {u['name']}")
                user_id = ask_int("id пользователя: ", 1)
                for v in vs.user_visits(visits, user_id):
                    place = pl.find_place(places, v["place_id"])
                    name = place["name"] if place else "?"
                    print(f"№{v['id']} {v['date']} {name}, "
                          f"{v['people']} чел., статус: {v['status']}")
            elif choice == "10":
                place = pl.add_place(
                    places,
                    name=input("Название: "),
                    category=input("Категория: "),
                    address=input("Адрес: "),
                    price=ask_float("Цена на человека: "),
                    capacity=ask_int("Вместимость: ", 1),
                    open_hour=ask_int("Открывается в (час): "),
                    close_hour=ask_int("Закрывается в (час): "),
                )
                save_json(PLACES_FILE, places)
                print(f"Добавлено место №{place['id']}")
            else:
                print("Нет такого пункта")
        except ValueError as error:
            print(f"Ошибка: {error}")
        except OSError as error:
            print(f"Ошибка записи файла: {error}")


if __name__ == "__main__":
    main()
