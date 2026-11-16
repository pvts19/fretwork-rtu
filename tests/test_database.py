"""Проверка SQL-запросов на временной копии базы."""
import pytest

from db import database
from db import import_json
from db import queries as q


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.sqlite")
    monkeypatch.setattr(import_json, "DB_PATH", tmp_path / "test.sqlite")
    monkeypatch.setattr(database.get_connection, "__defaults__",
                        (tmp_path / "test.sqlite",))
    import_json.main()


def test_place_list_and_filters():
    assert len(database.fetch_all(q.PLACE_LIST)) == 6
    cafes = database.fetch_all(q.PLACES_BY_CATEGORY, {"category": "Кафе"})
    assert {p["category"] for p in cafes} == {"Кафе"}


def test_free_places_ignore_cancelled():
    free = database.fetch_all(q.FREE_PLACES,
                              {"date": "2026-12-05", "people": 5})
    names = [p["name"] for p in free]
    assert "База отдыха «Сосны»" not in names  # занято 28 из 30


def test_visit_detail_join():
    visit = database.fetch_one(q.VISIT_DETAIL, {"id": 1})
    assert visit["place_name"] == "Кафе «Веранда»"
    assert visit["cost"] == 1200 * 4


def test_totals():
    totals = database.fetch_one(q.TOTALS)
    assert totals["visits"] == 6 and totals["active"] == 2
