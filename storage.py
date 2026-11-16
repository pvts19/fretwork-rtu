"""Загрузка и сохранение объектов проекта в JSON-файлах."""
import json
from pathlib import Path

from models import Entity, Place, User, Visit

DATA_DIR = Path(__file__).resolve().parent / "data"
PLACES_FILE = DATA_DIR / "places.json"
USERS_FILE = DATA_DIR / "users.json"
VISITS_FILE = DATA_DIR / "visits.json"


def load_json(path: Path) -> list[dict]:
    """Читает список записей из JSON. Нет файла — пустой список."""
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError(f"Файл {path.name} повреждён: {error}") from error
    if not isinstance(data, list):
        raise ValueError(f"В файле {path.name} ожидается список записей")
    return data


def save_json(path: Path, data: list[dict]) -> None:
    """Сохраняет список записей в JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_objects(path: Path, cls: type[Entity]) -> list:
    """Загружает JSON и создаёт из каждой записи объект класса cls."""
    try:
        return [cls.from_dict(item) for item in load_json(path)]
    except TypeError as error:
        raise ValueError(f"Неверная структура {path.name}: {error}") from error


def save_objects(path: Path, objects: list[Entity]) -> None:
    """Сохраняет объекты в JSON."""
    save_json(path, [obj.to_dict() for obj in objects])


def load_places() -> list[Place]:
    return load_objects(PLACES_FILE, Place)


def load_users() -> list[User]:
    return load_objects(USERS_FILE, User)


def load_visits() -> list[Visit]:
    return load_objects(VISITS_FILE, Visit)
