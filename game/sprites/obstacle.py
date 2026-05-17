"""Модуль спрайтов-препятствий."""

from abc import ABC, abstractmethod

from .sprite import Sprite


class Obstacle(Sprite, ABC):
    """Непроходимое препятствие."""

    color = "red"

    @abstractmethod
    def __init__(self, x: int, y: int) -> None:
        """Инициализирует препятствие."""
        super().__init__(x, y)


class Wall(Obstacle):
    """Стена."""

    img = "█"
    name = "стена"

    def __init__(self, x: int, y: int) -> None:
        """Инициализация."""
        super().__init__(x, y)


class Fence(Obstacle):
    """Забор."""

    img = "#"
    name = "забор"

    def __init__(self, x: int, y: int) -> None:
        """Инициализация."""
        super().__init__(x, y)
