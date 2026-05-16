"""Модуль подбираемых спрайтов."""

from abc import ABC, abstractmethod

from game.models import Event

from .sprite import Sprite


class Collectable(Sprite, ABC):
    """Подбираемый предмет."""

    img = "?"

    @abstractmethod
    def __init__(self, x: int, y: int) -> None:
        """Инициализирует предмет."""
        super().__init__(x, y)
        self.is_interactive = True
        self.is_solid = False
        self.name = "подбираемый предмет"
        self.img = "$"
        self.color = "white"


class Coin(Collectable):
    """Монета."""

    img = "●"

    def __init__(self, x: int, y: int) -> None:
        """Инициализирует монету."""
        super().__init__(x, y)
        self.name = "монета"
        self.color = "yellow"

    def interact(self, sprite: Sprite) -> Event | None:
        """Вызывается, когда на этот спрайт "наступает" игрок."""
        sprite.coins += 1
        return Event(f"{sprite.name} взял {self.name}", "collect")
