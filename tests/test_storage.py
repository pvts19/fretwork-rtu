import pytest

import storage
from models import Place


def test_save_and_load_objects(tmp_path):
    path = tmp_path / "places.json"
    place = Place(1, "Кафе", "Кафе", "ул. А", 500, 10, 10, 22)
    storage.save_objects(path, [place])
    loaded = storage.load_objects(path, Place)
    assert loaded == [place] and loaded[0].name == "Кафе"


def test_missing_file_gives_empty_list(tmp_path):
    assert storage.load_objects(tmp_path / "nope.json", Place) == []


def test_broken_file_raises(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{oops", encoding="utf-8")
    with pytest.raises(ValueError):
        storage.load_json(path)


def test_wrong_structure_raises(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text('[{"id": 1}]', encoding="utf-8")
    with pytest.raises(ValueError):
        storage.load_objects(path, Place)


def test_project_data_loads():
    assert storage.load_places() and storage.load_users()
    assert storage.load_visits()
