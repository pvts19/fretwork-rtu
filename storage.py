"""Загрузка и сохранение данных проекта в JSON-файлах."""
import json
from pathlib import Path

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
