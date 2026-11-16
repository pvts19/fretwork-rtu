import pytest

import visits as vs
from models import Place, User, Visit

FUTURE = "2099-01-01"


@pytest.fixture
def places():
    return [Place(1, "Кафе", "Кафе", "ул. А", 500, 10, 10, 22)]


@pytest.fixture
def visits():
    return [
        Visit(1, 1, 1, FUTURE, 6),
        Visit(2, 1, 2, FUTURE, 4, status="cancelled"),
        Visit(3, 1, 2, "2020-01-01", 2, status="done", rating=4),
    ]


def test_cancelled_visits_do_not_take_capacity(places, visits):
    assert places[0].free_capacity(visits, FUTURE) == 4


def test_create_visit_checks_capacity(places, visits):
    visit = vs.create_visit(visits, places, 1, 3, FUTURE, 4)
    assert visit.is_active
    with pytest.raises(ValueError):
        vs.create_visit(visits, places, 1, 3, FUTURE, 1)


def test_create_visit_rejects_past_date(places, visits):
    with pytest.raises(ValueError):
        vs.create_visit(visits, places, 1, 3, "2000-01-01", 1)


def test_cancel_only_active(visits):
    assert vs.cancel_visit(visits, 1).status == "cancelled"
    with pytest.raises(ValueError):
        vs.cancel_visit(visits, 1)


def test_complete_with_rating(visits):
    visits[0].complete(5)
    assert visits[0].status == "done" and visits[0].rating == 5


def test_visit_json_roundtrip(visits):
    data = visits[1].to_dict()
    assert data["status"] == "cancelled" and "_status" not in data
    assert Visit.from_dict(data).status == "cancelled"


def test_rating_and_available(places, visits):
    assert vs.place_rating(visits, 1) == 4
    assert vs.available_places(places, visits, FUTURE, 5) == []


def test_user_visits_sorted(visits):
    user = User(2, "Иван", "ivan@example.com")
    assert [v.id for v in user.visits(visits)] == [3, 2]
    with pytest.raises(ValueError):
        User(3, "Без почты", "nope")
