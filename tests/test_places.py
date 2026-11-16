import pytest

import place_service as pl
from models import Place


@pytest.fixture
def places():
    return [
        Place(1, "Парк", "Парк", "ул. А", 0, 100, 6, 24),
        Place(2, "Кафе", "Кафе", "ул. Б", 1000, 10, 20, 4),
    ]


def test_add_place_assigns_next_id(places):
    place = pl.add_place(places, "Музей", "Музей", "ул. В", 500, 50, 10, 18)
    assert place.id == 3
    assert len(places) == 3


def test_place_validation():
    with pytest.raises(ValueError):
        Place(1, "  ", "Музей", "ул. В", 500, 50, 10, 18)
    with pytest.raises(ValueError):
        Place(1, "Музей", "Музей", "ул. В", -1, 50, 10, 18)


def test_search_and_category(places):
    assert pl.search_places(places, "ул. б")[0].id == 2
    assert [p.id for p in pl.filter_by_category(places, "парк")] == [1]


def test_budget_filter(places):
    assert [p.id for p in pl.filter_by_budget(places, 1500, 2)] == [1]


def test_sort_places(places):
    assert pl.sort_places(places, "price", reverse=True)[0].id == 2
    with pytest.raises(ValueError):
        pl.sort_places(places, "unknown")


def test_is_open_at_through_midnight(places):
    assert places[1].is_open_at(23)
    assert places[1].is_open_at(2)
    assert not places[1].is_open_at(12)


def test_str_and_dict_roundtrip(places):
    assert "Кафе" in str(places[1])
    assert Place.from_dict(places[1].to_dict()) == places[1]
