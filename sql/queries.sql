-- SQL-запросы проекта RestSpot.
-- Проверка: sqlite3 data/restspot.sqlite < sql/queries.sql
-- В приложении (db/queries.py) значения передаются параметрами :name,
-- здесь подставлены примеры значений.

-- 1. Список всех мест (выборка)
SELECT p.id, p.name, p.category, p.address, p.price, p.capacity,
    p.open_hour || ':00–' || p.close_hour || ':00' AS hours FROM places p ORDER BY p.name;

-- 2. Места заданной категории (WHERE)
SELECT p.id, p.name, p.category, p.address, p.price, p.capacity,
    p.open_hour || ':00–' || p.close_hour || ':00' AS hours FROM places p
    WHERE p.category = 'Кафе' ORDER BY p.name;

-- 3. Поиск мест по названию или адресу (WHERE + LIKE)
SELECT p.id, p.name, p.category, p.address, p.price, p.capacity,
    p.open_hour || ':00–' || p.close_hour || ':00' AS hours FROM places p
    WHERE p.name LIKE '%Парк%' OR p.address LIKE '%Парк%' ORDER BY p.name;

-- 4. Места в пределах бюджета компании (WHERE)
SELECT p.id, p.name, p.category, p.address, p.price, p.capacity,
    p.open_hour || ':00–' || p.close_hour || ':00' AS hours, p.price * 3 AS total
    FROM places p WHERE p.price * 3 <= 2500 ORDER BY total;

-- 5. Посещения с местом и пользователем (JOIN)
SELECT v.id, v.date, v.people, v.status, v.rating,
    CASE v.status WHEN 'active' THEN 'активно'
    WHEN 'cancelled' THEN 'отменено' ELSE 'завершено' END AS status_label, p.id AS place_id, p.name AS place_name,
    u.name AS user_name
    FROM visits v
    JOIN places p ON p.id = v.place_id
    JOIN users u ON u.id = v.user_id
    WHERE ('' = '' OR v.status = '')
    ORDER BY v.date;

-- 6. Полная информация о посещении (JOIN)
SELECT v.id, v.date, v.people, v.status, v.rating,
    CASE v.status WHEN 'active' THEN 'активно'
    WHEN 'cancelled' THEN 'отменено' ELSE 'завершено' END AS status_label, p.id AS place_id, p.name AS place_name,
    p.price * v.people AS cost, u.name AS user_name, u.email AS user_email
    FROM visits v
    JOIN places p ON p.id = v.place_id
    JOIN users u ON u.id = v.user_id
    WHERE v.id = 1;

-- 7. Свободные места на дату (LEFT JOIN + GROUP BY + HAVING)
SELECT p.id, p.name, p.category, p.address, p.price, p.capacity,
    p.open_hour || ':00–' || p.close_hour || ':00' AS hours,
    p.capacity - COALESCE(SUM(v.people), 0) AS free
    FROM places p
    LEFT JOIN visits v
    ON v.place_id = p.id AND v.date = '2026-12-05' AND v.status = 'active'
    GROUP BY p.id
    HAVING free >= 5
    ORDER BY free DESC;

-- 8. Количество посещений по статусам (COUNT + GROUP BY)
SELECT v.status, CASE v.status WHEN 'active' THEN 'активно'
    WHEN 'cancelled' THEN 'отменено' ELSE 'завершено' END AS status_label, COUNT(*) AS cnt,
    SUM(v.people) AS people
    FROM visits v GROUP BY v.status ORDER BY cnt DESC;

-- 9. Количество посещений по местам (COUNT + GROUP BY)
SELECT p.id, p.name, COUNT(v.id) AS cnt,
    COALESCE(SUM(v.people), 0) AS people
    FROM places p LEFT JOIN visits v ON v.place_id = p.id
    GROUP BY p.id ORDER BY cnt DESC, p.name;

-- 10. Средний рейтинг мест (AVG + GROUP BY)
SELECT p.id, p.name, ROUND(AVG(v.rating), 1) AS rating,
    COUNT(v.rating) AS marks
    FROM places p JOIN visits v ON v.place_id = p.id
    WHERE v.rating IS NOT NULL
    GROUP BY p.id ORDER BY rating DESC;

-- 11. Места, где посещений больше N (GROUP BY + HAVING)
SELECT p.id, p.name, COUNT(v.id) AS cnt
    FROM places p JOIN visits v ON v.place_id = p.id
    WHERE v.status <> 'cancelled'
    GROUP BY p.id HAVING COUNT(v.id) > 1 ORDER BY cnt DESC;

-- 12. Общая статистика (COUNT, SUM, AVG)
SELECT
    (SELECT COUNT(*) FROM places) AS places,
    (SELECT COUNT(*) FROM users) AS users,
    COUNT(*) AS visits,
    SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS active,
    SUM(people) AS people,
    ROUND(AVG(rating), 1) AS avg_rating
    FROM visits;
