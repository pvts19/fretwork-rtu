"""Место отдыха."""
from models.base import Entity


class Place(Entity):
    """Место отдыха: парк, кафе, пляж, музей и т. п."""

    def __init__(self, id: int, name: str, category: str, address: str,
                 price: float, capacity: int, open_hour: int,
                 close_hour: int) -> None:
        super().__init__(id)
        if not name.strip():
            raise ValueError("Название не может быть пустым")
        if price < 0 or capacity <= 0:
            raise ValueError("Цена должна быть >= 0, вместимость > 0")
        if not (0 <= open_hour <= 24 and 0 <= close_hour <= 24):
            raise ValueError("Часы работы должны быть от 0 до 24")
        self.name = name.strip()
        self.category = category.strip()
        self.address = address.strip()
        self.price = price
        self.capacity = capacity
        self.open_hour = open_hour
        self.close_hour = close_hour

    def cost(self, people: int) -> float:
        """Стоимость посещения для компании из people человек."""
        return self.price * people

    def is_open_at(self, hour: int) -> bool:
        """Открыто ли место в указанный час."""
        if self.open_hour <= self.close_hour:
            return self.open_hour <= hour < self.close_hour
        return hour >= self.open_hour or hour < self.close_hour

    def people_on(self, visits: list, day: str,
                  exclude_id: int | None = None) -> int:
        """Сколько человек записано на дату (только активные посещения)."""
        return sum(v.people for v in visits
                   if v.place_id == self.id and v.date == day
                   and v.is_active and v.id != exclude_id)

    def free_capacity(self, visits: list, day: str) -> int:
        """Свободная вместимость места на дату."""
        return self.capacity - self.people_on(visits, day)

    @property
    def hours(self) -> str:
        return f"{self.open_hour}:00–{self.close_hour}:00"

    def __str__(self) -> str:
        return (f"[{self.id}] {self.name} ({self.category}) — {self.address}, "
                f"{self.price} руб./чел., до {self.capacity} чел., "
                f"{self.hours}")
