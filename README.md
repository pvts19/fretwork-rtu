# RestSpot — сервис поиска мест для отдыха

## Назначение

RestSpot помогает быстро найти, где провести свободное время: парк, кафе,
пляж, музей, базу отдыха и т. п. Пользователь указывает бюджет, количество
человек и желаемую категорию, а сервис подсказывает, подходит ли место по
цене, открыто ли оно сейчас и сколько будет стоить поход.

## Целевая аудитория

- студенты и молодёжь, которые ищут, куда сходить после учёбы или на выходных;
- семьи и компании друзей, планирующие совместный отдых;
- туристы, впервые оказавшиеся в городе.

## Предметная область

Места для отдыха в городе и за его пределами. У каждого места есть
категория, адрес, часы работы, средняя стоимость посещения на человека и
рейтинг, который складывается из отзывов пользователей. Пользователи ищут
места по категории и бюджету, добавляют их в избранное и оставляют отзывы.

## Основные сущности

- **Место отдыха (Place)** — название, категория (парк, кафе, пляж, музей,
  база отдыха…), адрес, цена на человека, вместимость, часы работы;
- **Пользователь (User)** — имя, e-mail;
- **Посещение (Visit)** — запланированный поход пользователя в место:
  дата, количество человек, статус (активно / отменено / завершено) и
  оценка 1–5 после посещения (из оценок складывается рейтинг места).

## Основные функции

- просмотр, поиск и добавление мест отдыха;
- отбор мест по категории и по бюджету компании;
- сортировка мест по названию, цене, вместимости;
- проверка, открыто ли место в данный момент;
- поиск мест со свободной вместимостью на выбранную дату;
- планирование и отмена посещений;
- рейтинг мест по оценкам пользователей.

## Объектная модель

| Класс | Атрибуты | Методы |
|---|---|---|
| `Entity` (базовый) | `id` | `to_dict()`, `from_dict()` (`@classmethod`), `__eq__`, `__repr__` |
| `Place(Entity)` | `name`, `category`, `address`, `price`, `capacity`, `open_hour`, `close_hour` | `cost(people)`, `is_open_at(hour)`, `people_on(visits, day)`, `free_capacity(visits, day)`, свойство `hours`, `__str__` |
| `User(Entity)` | `name`, `email` | `visits(visits)`, `__str__` |
| `Visit(Entity)` | `place_id`, `user_id`, `date`, `people`, `_status`, `rating` | свойства `status`, `is_active`; `cancel()`, `complete(rating)` (декоратор `@only_active`), `is_past()` (`@staticmethod`), `to_dict()`, `__str__` |

Взаимодействие объектов: `Place.free_capacity()` считает занятость по
объектам `Visit`, `User.visits()` отбирает посещения пользователя, функции
`visits.create_visit()` / `cancel_visit()` связывают место, пользователя и
посещение. Статус посещения инкапсулирован (`_status`) и меняется только
методами `cancel()` / `complete()`.

## Структура проекта

```
restspot/
├── main.py            # меню консольного приложения
├── models/            # классы Entity, Place, User, Visit
├── place_service.py   # функции работы с коллекцией мест
├── visit_service.py   # функции работы с коллекцией посещений
├── storage.py         # загрузка/сохранение объектов в JSON
├── utils.py           # ввод и вывод в консоли
├── data/              # places.json, users.json, visits.json
├── tests/             # тесты pytest
├── manage.py          # управление Django-проектом
├── restspot/          # настройки Django: settings.py, urls.py
├── homepage/          # приложение «Главная страница»
├── places/            # приложение «Места отдыха»
└── visits/            # приложение «Посещения»
```

В ПР5 модули `places.py` / `visits.py` консольной версии переименованы в
`place_service.py` / `visit_service.py`, чтобы освободить имена для
Django-приложений.

## Веб-приложение (Django)

| URL | Имя маршрута | Шаблон | Страница |
|---|---|---|---|
| `/` | `homepage:index` | `homepage/index.html` | главная |
| `/places/` | `places:list` | `places/place_list.html` | список мест |
| `/places/<id>/` | `places:detail` | `places/place_detail.html` | карточка места |
| `/visits/` | `visits:list` | `visits/visit_list.html` | список посещений |
| `/visits/<id>/` | `visits:detail` | `visits/visit_detail.html` | карточка посещения |

Шаблоны (`templates/`): базовый `base.html` с блоками `title` и
`content`, включаемые `includes/navbar.html`, `includes/footer.html`,
`includes/place_card.html`. Используются `{% for %}…{% empty %}`, `{% if %}`,
`{% url %}` с пространствами имён, фильтры `date`, `floatformat`, `default`,
`pluralize`, `truncatechars`, `upper`, `lower`, `capfirst`.

Статика (`static/`): `css/style.css` — собственное оформление поверх
Bootstrap 5, `img/logo.svg`, `img/hero.svg`, `js/main.js` — быстрый фильтр
карточек на странице мест. Данные берутся из JSON через классы ПР3.
Для несуществующих объектов возвращается 404.

```bash
python manage.py check
python manage.py runserver    # http://127.0.0.1:8000/
```

## База данных SQLite (ПР7)

Структура (`sql/schema.sql`):

| Таблица | Поля | Ключи |
|---|---|---|
| `places` | id, name, category, address, price, capacity, open_hour, close_hour | PK `id` |
| `users` | id, name, email (UNIQUE) | PK `id` |
| `visits` | id, place_id, user_id, date, people, status, rating (NULL — нет оценки) | PK `id`, FK `place_id → places.id`, FK `user_id → users.id` |

Файлы:

- `sql/schema.sql` — создание таблиц;
- `sql/queries.sql` — 12 проверенных запросов (выборка, WHERE, JOIN,
  COUNT/SUM/AVG, GROUP BY, HAVING);
- `db/database.py` — подключение (`row_factory = sqlite3.Row`,
  `PRAGMA foreign_keys = ON`), функции `fetch_all` / `fetch_one`;
- `db/queries.py` — те же запросы с параметрами `:name` для представлений;
- `db/import_json.py` — создание базы и перенос данных из JSON;
- `data/restspot.sqlite` — файл базы.

```bash
python -m db.import_json                    # пересоздать базу из JSON
sqlite3 data/restspot.sqlite < sql/queries.sql
```

Новые страницы: `/places/free/?date=…&people=…` — места со свободной
вместимостью на дату (учитываются только активные посещения),
`/visits/stats/` — статистика. На странице мест работают поиск (`?q=`) и
фильтр по категории (`?category=`), на странице посещений — фильтр по
статусу. Все значения передаются в запросы только параметрами.

Ограничение: в SQLite `LIKE` без учёта регистра работает только для
латиницы, поэтому поиск по русскому тексту чувствителен к регистру.

## Django ORM (ПР9)

Начиная с ПР9 веб-приложение работает с базой `db.sqlite3` через модели
Django, прямые SQL-запросы из представлений убраны (модуль `db/` и файлы
`sql/` сохранены как результат ПР7 и используются для переноса данных).

| Модель | Приложение | Поля | Связи |
|---|---|---|---|
| `Place` | `places` | name, category (choices), address, price, capacity, open_hour, close_hour | `visits` — обратная связь |
| `User` | `users` | name, email (unique) | `visits` — обратная связь |
| `Visit` | `visits` | date, people, status (choices), rating | `place` → Place, `user` → User (`on_delete=CASCADE`, `related_name='visits'`) |

Первый запуск:

```bash
python manage.py migrate
python -m db.import_json        # база ПР7 из JSON (если её нет)
python manage.py import_data    # перенос в модели Django с сохранением id
python manage.py runserver
```

Что реализовано через ORM:

- список мест: поиск `Q(name__icontains) | Q(address__icontains)`, фильтр по
  категории и цене, сортировка (название, цена, рейтинг, популярность),
  `annotate(Avg, Count)`, пагинация `Paginator` по 6 мест;
- карточка места: `get_object_or_404`, активные посещения через
  `place.visits` + `select_related('user')`;
- свободные места на дату: `annotate(Sum(..., filter=Q(...)))`,
  отменённые посещения вместимость не занимают;
- список посещений: `select_related('place', 'user')`, фильтры по статусу,
  дате, месту, пользователю, сортировка, пагинация с сохранением фильтров;
- статистика: `aggregate(Count, Sum, Avg, Min, Max)`,
  `values('status').annotate(...)`, `filter(cnt__gt=1)`;
- некорректные GET-параметры игнорируются, отсутствующие объекты — 404.

Тесты Django (`tests/test_orm.py`) запускаются через `pytest` (pytest-django).

## Запуск

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py       # консольное приложение
pytest               # тесты
flake8               # проверка оформления кода
```

## План развития

На следующих этапах планируется:

- хранение списка мест в коллекциях и JSON-файлах (ПР2);
- описание сущностей в виде классов (ПР3);
- разработка веб-приложения на Django (ПР5–ПР6);
- подключение базы данных (ПР7, ПР9);
- административная панель и формы (ПР10–ПР11);
- реализация пользователей и авторизации;
- разработка API;
- контейнеризация приложения;
- настройка CI/CD.
