import pytest

import visits as vs

FUTURE = "2099-01-01"


@pytest.fixture
def places():
    return [{"id": 1, "name": "Кафе", "category": "Кафе", "address": "ул. А",
             "price": 500, "capacity": 10, "open_hour": 10,
             "close_hour": 22}]


@pytest.fixture
def visits():
    return [
        {"id": 1, "place_id": 1, "user_id": 1, "date": FUTURE, "people": 6,
         "status": "active", "rating": None},
        {"id": 2, "place_id": 1, "user_id": 2, "date": FUTURE, "people": 4,
         "status": "cancelled", "rating": None},
        {"id": 3, "place_id": 1, "user_id": 2, "date": "2020-01-01",
         "people": 2, "status": "done", "rating": 4},
    ]


def test_cancelled_visits_do_not_take_capacity(places, visits):
    assert vs.free_capacity(places[0], visits, FUTURE) == 4


def test_create_visit_checks_capacity(places, visits):
    visit = vs.create_visit(visits, places, 1, 3, FUTURE, 4)
    assert visit["status"] == "active"
    with pytest.raises(ValueError):
        vs.create_visit(visits, places, 1, 3, FUTURE, 1)


def test_create_visit_rejects_past_date(places, visits):
    with pytest.raises(ValueError):
        vs.create_visit(visits, places, 1, 3, "2000-01-01", 1)


def test_cancel_visit(visits):
    assert vs.cancel_visit(visits, 1)["status"] == "cancelled"
    with pytest.raises(ValueError):
        vs.cancel_visit(visits, 1)


def test_rating_and_available(places, visits):
    assert vs.place_rating(visits, 1) == 4
    assert vs.available_places(places, visits, FUTURE, 5) == []
