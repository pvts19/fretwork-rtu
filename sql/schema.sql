-- Схема базы данных RestSpot (SQLite)
-- Скрипт пересоздаёт таблицы, поэтому импорт можно запускать повторно.
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS visits;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS users;

CREATE TABLE places (
    id         INTEGER PRIMARY KEY,
    name       TEXT    NOT NULL,
    category   TEXT    NOT NULL,
    address    TEXT    NOT NULL,
    price      REAL    NOT NULL CHECK (price >= 0),
    capacity   INTEGER NOT NULL CHECK (capacity > 0),
    open_hour  INTEGER NOT NULL CHECK (open_hour BETWEEN 0 AND 24),
    close_hour INTEGER NOT NULL CHECK (close_hour BETWEEN 0 AND 24)
);

CREATE TABLE users (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE visits (
    id       INTEGER PRIMARY KEY,
    place_id INTEGER NOT NULL REFERENCES places (id) ON DELETE CASCADE,
    user_id  INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    date     TEXT    NOT NULL,              -- ГГГГ-ММ-ДД
    people   INTEGER NOT NULL CHECK (people > 0),
    status   TEXT    NOT NULL DEFAULT 'active'
             CHECK (status IN ('active', 'cancelled', 'done')),
    rating   INTEGER CHECK (rating BETWEEN 1 AND 5)  -- NULL, если оценки нет
);

CREATE INDEX idx_visits_place_date ON visits (place_id, date);
