"""Модуль NPC."""

from abc import ABC, abstractmethod

from game.models import Event

from .sprite import Sprite


class Npc(Sprite, ABC):
    """Непись."""

    img = "?"
    name = "NPC"
    color = "green"

    @ abstractmethod
    def __init__(self, x: int, y: int) -> None:
        """Инициализирует спрайт."""
        super().__init__(x, y)
        self.is_interactive = True
        self.message = "бу-бу-бу"

    def interact(self, _: Sprite) -> Event | None:
        """NPC возвращает событие со своим сообщением."""
        return Event(message=f"{self.name}: {self.message}", sound="talk")


class Anakondova(Npc):
    """Анна Анакондова."""

    img = "A"

    def __init__(self, x: int, y: int) -> None:
        """Инициализирует спрайт."""
        super().__init__(x, y)
        self.name = "Анна Анакондова"
        self.message = "Привет!"


class Gadukin(Npc):
    """Гена Гадюкин."""

    img = "G"

    def __init__(self, x: int, y: int) -> None:
        """Инициализирует спрайт."""
        super().__init__(x, y)
        self.name = "Гена Гадюкин"
        self.message = "Здравствуй!"
