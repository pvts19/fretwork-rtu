import pytest

import places as pl


@pytest.fixture
def places():
    return [
        {"id": 1, "name": "Парк", "category": "Парк", "address": "ул. А",
         "price": 0, "capacity": 100, "open_hour": 6, "close_hour": 24},
        {"id": 2, "name": "Кафе", "category": "Кафе", "address": "ул. Б",
         "price": 1000, "capacity": 10, "open_hour": 20, "close_hour": 4},
    ]


def test_add_place_assigns_next_id(places):
    place = pl.add_place(places, "Музей", "Музей", "ул. В", 500, 50, 10, 18)
    assert place["id"] == 3
    assert len(places) == 3


def test_add_place_rejects_empty_name(places):
    with pytest.raises(ValueError):
        pl.add_place(places, "  ", "Музей", "ул. В", 500, 50, 10, 18)


def test_search_and_category(places):
    assert pl.search_places(places, "ул. б")[0]["id"] == 2
    assert [p["id"] for p in pl.filter_by_category(places, "парк")] == [1]


def test_budget_filter(places):
    assert [p["id"] for p in pl.filter_by_budget(places, 1500, 2)] == [1]


def test_sort_places(places):
    assert pl.sort_places(places, "price", reverse=True)[0]["id"] == 2
    with pytest.raises(ValueError):
        pl.sort_places(places, "unknown")


def test_is_open_at_through_midnight(places):
    assert pl.is_open_at(places[1], 23)
    assert pl.is_open_at(places[1], 2)
    assert not pl.is_open_at(places[1], 12)
