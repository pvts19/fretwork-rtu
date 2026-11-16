"""Подключение к базе SQLite и выполнение запросов."""
import sqlite3
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "restspot.sqlite"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection(path: Path = DB_PATH) -> sqlite3.Connection:
    """Открывает соединение: строки как sqlite3.Row, внешние ключи включены."""
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _to_dict(row: sqlite3.Row) -> dict:
    data = dict(row)
    if isinstance(data.get("date"), str):
        data["day"] = date.fromisoformat(data["date"])
    return data


def fetch_all(sql: str, params: tuple | dict = ()) -> list[dict]:
    """Выполняет SELECT (только параметризованный) и возвращает словари."""
    with get_connection() as conn:
        return [_to_dict(row) for row in conn.execute(sql, params)]


def fetch_one(sql: str, params: tuple | dict = ()) -> dict | None:
    rows = fetch_all(sql, params)
    return rows[0] if rows else None
