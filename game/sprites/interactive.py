"""Модуль интерактивных спрайтов."""

from .sprite import Sprite


class Door(Sprite):
    """Дверь."""

    img = "D"

    def __init__(self, x: int, y: int) -> None:
        """Инициализирует дверь."""
        super().__init__(x, y)
        self.name = "дверь"
        self.color = "magenta"
        self.is_solid = False
        self.is_interactive = True
