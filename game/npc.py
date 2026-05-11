"""Модуль NPC."""

from .event import Event
from .sprite import Sprite


class Npc(Sprite):
    """Непись."""

    def __init__(self, x: int, y: int) -> None:
        """Инициализирует спрайт."""
        super().__init__(x, y)
        self.name = "NPC"
        self.img = "N"
        self.color = "green"
        self.message = "бу-бу-бу"

    def interact(self, _: Sprite) -> Event | None:
        """NPC возвращает событие со своим сообщением."""
        return Event(message=f"{self.name}: {self.message}", sound="talk")


class Anakondova(Npc):
    """Непись."""

    def __init__(self, x: int, y: int) -> None:
        """Инициализирует спрайт."""
        super().__init__(x, y)
        self.name = "Анна Анакондова"
        self.img = "A"
        self.message = "Привет!"


class Gadukin(Npc):
    """Непись."""

    def __init__(self, x: int, y: int) -> None:
        """Инициализирует спрайт."""
        super().__init__(x, y)
        self.name = "Гена Гадюкин"
        self.img = "G"
        self.message = "Здравствуй!"
