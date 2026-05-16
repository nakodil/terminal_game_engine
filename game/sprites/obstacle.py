"""Модуль спрайтов-препятствий."""

from abc import ABC, abstractmethod

from .sprite import Sprite


class Obstacle(Sprite, ABC):
    """Непроходимое препятствие."""

    @abstractmethod
    def __init__(self, x: int, y: int) -> None:
        """Инициализирует препятствие."""
        super().__init__(x, y)
        self.color = "red"


class Wall(Obstacle):
    """Стена."""

    img = "█"

    def __init__(self, x: int, y: int) -> None:
        """Инициализация."""
        super().__init__(x, y)


class Fence(Obstacle):
    """Забор."""

    img = "#"

    def __init__(self, x: int, y: int) -> None:
        """Инициализация."""
        super().__init__(x, y)
