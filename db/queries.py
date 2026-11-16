"""SQL-запросы проекта (те же, что в sql/queries.sql), для представлений."""

PLACE_FIELDS = """p.id, p.name, p.category, p.address, p.price, p.capacity,
    p.open_hour || ':00–' || p.close_hour || ':00' AS hours"""

STATUS_LABEL = """CASE v.status WHEN 'active' THEN 'активно'
    WHEN 'cancelled' THEN 'отменено' ELSE 'завершено' END AS status_label"""

# 1. Список всех мест
PLACE_LIST = f"SELECT {PLACE_FIELDS} FROM places p ORDER BY p.name"

# 2. Места заданной категории (WHERE)
PLACES_BY_CATEGORY = f"""SELECT {PLACE_FIELDS} FROM places p
    WHERE p.category = :category ORDER BY p.name"""

# 3. Поиск мест по названию или адресу (WHERE + LIKE)
PLACES_SEARCH = f"""SELECT {PLACE_FIELDS} FROM places p
    WHERE p.name LIKE :text OR p.address LIKE :text ORDER BY p.name"""

# 4. Места, укладывающиеся в бюджет компании (WHERE с вычислением)
PLACES_BY_BUDGET = f"""SELECT {PLACE_FIELDS}, p.price * :people AS total
    FROM places p WHERE p.price * :people <= :budget ORDER BY total"""

# Одно место по id
PLACE_BY_ID = f"SELECT {PLACE_FIELDS} FROM places p WHERE p.id = :id"

# Список категорий
CATEGORIES = "SELECT DISTINCT category FROM places ORDER BY category"

# 5. Посещения со сведениями о месте и пользователе (JOIN)
VISIT_LIST = f"""SELECT v.id, v.date, v.people, v.status, v.rating,
    {STATUS_LABEL}, p.id AS place_id, p.name AS place_name,
    u.name AS user_name
    FROM visits v
    JOIN places p ON p.id = v.place_id
    JOIN users u ON u.id = v.user_id
    WHERE (:status = '' OR v.status = :status)
    ORDER BY v.date"""

# 6. Полная информация о посещении (JOIN)
VISIT_DETAIL = f"""SELECT v.id, v.date, v.people, v.status, v.rating,
    {STATUS_LABEL}, p.id AS place_id, p.name AS place_name,
    p.price * v.people AS cost, u.name AS user_name, u.email AS user_email
    FROM visits v
    JOIN places p ON p.id = v.place_id
    JOIN users u ON u.id = v.user_id
    WHERE v.id = :id"""

# Активные посещения места (WHERE)
PLACE_ACTIVE_VISITS = """SELECT id, date, people FROM visits
    WHERE place_id = :id AND status = 'active' ORDER BY date"""

# 7. Места со свободной вместимостью на дату (LEFT JOIN + GROUP BY + HAVING)
FREE_PLACES = f"""SELECT {PLACE_FIELDS},
    p.capacity - COALESCE(SUM(v.people), 0) AS free
    FROM places p
    LEFT JOIN visits v
        ON v.place_id = p.id AND v.date = :date AND v.status = 'active'
    GROUP BY p.id
    HAVING free >= :people
    ORDER BY free DESC"""

# 8. Количество посещений по статусам (агрегат + GROUP BY)
VISITS_BY_STATUS = f"""SELECT v.status, {STATUS_LABEL}, COUNT(*) AS cnt,
    SUM(v.people) AS people
    FROM visits v GROUP BY v.status ORDER BY cnt DESC"""

# 9. Количество посещений по местам (LEFT JOIN + GROUP BY)
VISITS_BY_PLACE = """SELECT p.id, p.name, COUNT(v.id) AS cnt,
    COALESCE(SUM(v.people), 0) AS people
    FROM places p LEFT JOIN visits v ON v.place_id = p.id
    GROUP BY p.id ORDER BY cnt DESC, p.name"""

# 10. Средний рейтинг мест (AVG + GROUP BY)
PLACE_RATINGS = """SELECT p.id, p.name, ROUND(AVG(v.rating), 1) AS rating,
    COUNT(v.rating) AS marks
    FROM places p JOIN visits v ON v.place_id = p.id
    WHERE v.rating IS NOT NULL
    GROUP BY p.id ORDER BY rating DESC"""

# Рейтинг одного места (AVG)
PLACE_RATING = """SELECT ROUND(AVG(rating), 1) AS rating FROM visits
    WHERE place_id = :id AND rating IS NOT NULL"""

# 11. Места, у которых посещений больше N (GROUP BY + HAVING)
POPULAR_PLACES = """SELECT p.id, p.name, COUNT(v.id) AS cnt
    FROM places p JOIN visits v ON v.place_id = p.id
    WHERE v.status <> 'cancelled'
    GROUP BY p.id HAVING COUNT(v.id) > :min_count ORDER BY cnt DESC"""

# 12. Общая статистика (COUNT, SUM, AVG)
TOTALS = """SELECT
    (SELECT COUNT(*) FROM places) AS places,
    (SELECT COUNT(*) FROM users) AS users,
    COUNT(*) AS visits,
    SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS active,
    SUM(people) AS people,
    ROUND(AVG(rating), 1) AS avg_rating
    FROM visits"""
