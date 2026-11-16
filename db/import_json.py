"""Создаёт базу data/restspot.sqlite по sql/schema.sql и переносит в неё
данные из JSON-файлов.

Запуск:  python -m db.import_json
"""
from db.database import DB_PATH, SCHEMA_PATH, get_connection
from storage import load_places, load_users, load_visits


def main() -> None:
    places, users, visits = load_places(), load_users(), load_visits()
    with get_connection() as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.executemany(
            "INSERT INTO places VALUES (:id, :name, :category, :address, "
            ":price, :capacity, :open_hour, :close_hour)",
            [p.to_dict() for p in places])
        conn.executemany(
            "INSERT INTO users VALUES (:id, :name, :email)",
            [u.to_dict() for u in users])
        conn.executemany(
            "INSERT INTO visits VALUES (:id, :place_id, :user_id, :date, "
            ":people, :status, :rating)",
            [v.to_dict() for v in visits])
    print(f"База {DB_PATH.name}: мест {len(places)}, пользователей "
          f"{len(users)}, посещений {len(visits)}")


if __name__ == "__main__":
    main()
