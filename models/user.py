"""Пользователь сервиса."""
from models.base import Entity


class User(Entity):
    """Пользователь, который планирует посещения."""

    def __init__(self, id: int, name: str, email: str) -> None:
        super().__init__(id)
        if "@" not in email:
            raise ValueError("Некорректный e-mail")
        self.name = name.strip()
        self.email = email.strip()

    def visits(self, visits: list) -> list:
        """Посещения пользователя, отсортированные по дате."""
        return sorted((v for v in visits if v.user_id == self.id),
                      key=lambda v: v.date)

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} <{self.email}>"
