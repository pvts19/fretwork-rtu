import pytest

from storage import load_json, save_json


def test_save_and_load(tmp_path):
    path = tmp_path / "data.json"
    save_json(path, [{"id": 1, "name": "Кафе"}])
    assert load_json(path) == [{"id": 1, "name": "Кафе"}]


def test_missing_file_gives_empty_list(tmp_path):
    assert load_json(tmp_path / "nope.json") == []


def test_broken_file_raises(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{oops", encoding="utf-8")
    with pytest.raises(ValueError):
        load_json(path)
