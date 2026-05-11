"""Модуль интерактивных спрайтов."""

from .sprite import Sprite


class Door(Sprite):
    """Дверь."""

    def __init__(self, x: int, y: int) -> None:
        """Инициализирует дверь."""
        super().__init__(x, y)
        self.img = "D"
        self.color = "magenta"
        self.is_solid = False
