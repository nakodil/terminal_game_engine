"""Модуль спрайта."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.models import Event


class Sprite(ABC):
    """Спрайт – игровой объект на поле."""

    img = "?"

    @abstractmethod
    def __init__(
        self,
        x: int,
        y: int,
    ) -> None:
        """Инициализирует спрайт."""
        self.is_solid = True  # Спрайты не проходят сквозь друг друга
        self.x, self.y = x, y  # Как запретить спавн на занятые клетки?
        self.name = "Cпрайт"
        self.color = "white"
        self.speed = 0
        self.hp = 100
        self.hp_max = self.hp
        self.coins = 0
        self.is_visible = True
        self.is_interactive = False
        self.message = "Привет!"
        self.min_x, self.min_y = 0, 0
        self.max_x, self.max_y = 0, 0

    def setup(self, x_max: int, y_max: int) -> None:
        """Задает границы движения."""
        self.max_x = x_max
        self.max_y = y_max

    def update(self, _: str, __: list[Sprite]) -> bool:
        """Обновление."""
        return False

    def interact(self, _: Sprite) -> Event | None:
        """Вызывается, когда на этот спрайт "наступает" игрок."""
        return None

    def move(self, delta_x: int, delta_y: int, sprites: list[Sprite]) -> bool:
        """Движение.

        Вычисляет новые координаты;
        Проверяет выход за пределы "экрана";
        Проверяет столкновения с препятствиями;
        Задает спрайту новые координаты.
        Возвращает True, если спрайт смог двинуться.
        """
        new_x = self.x + delta_x
        new_y = self.y + delta_y

        if self.is_offscreen(new_x, new_y):
            return False

        if self.is_colliding_solid_sprite(new_x, new_y, sprites):
            return False

        self.x, self.y = new_x, new_y
        return True

    def is_colliding_solid_sprite(
            self, x: int, y: int, sprites: list[Sprite],
    ) -> bool:
        """Коллизии с другими спрайтами."""
        for sprite in sprites:
            if (
                sprite.is_solid
                and sprite.x == x
                and sprite.y == y
            ):
                return True
        return False

    def is_offscreen(self, x: int, y: int) -> bool:
        """Проверка выхода за пределы "экрана"."""
        return (
            x < self.min_x or x > self.max_x
            or
            y < self.min_y or y > self.max_y
        )
