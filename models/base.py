"""Базовый класс сущностей."""


class Entity:
    """Общий предок всех сущностей: идентификатор и (де)сериализация."""

    def __init__(self, id: int) -> None:
        self.id = id

    def to_dict(self) -> dict:
        """Словарь для сохранения в JSON (переопределяется в наследниках)."""
        return dict(vars(self))

    @classmethod
    def from_dict(cls, data: dict) -> "Entity":
        """Создаёт объект из словаря, прочитанного из JSON."""
        return cls(**data)

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and self.id == other.id

    def __repr__(self) -> str:
        return f"{type(self).__name__}(id={self.id})"
