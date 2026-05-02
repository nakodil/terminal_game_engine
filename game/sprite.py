"""Модуль спрайта."""

from abc import ABC, abstractmethod

import config


class Sprite(ABC):
    """Спрайт – игровой объект на поле."""

    @abstractmethod
    def __init__(self, x: int, y: int) -> None:
        """Инициализирует спрайт."""
        self.x, self.y = x, y  # Как запретить спавн на занятые клетки?
        self.min_x, self.min_y = 0, 0
        self.max_x, self.max_y = 0, 0
        self.img = "?"
        self.color = "red"
        self.is_visible = True
        self.speed = 0
        self._update_accumulator = 0.0

    def setup(self, x_max: int, y_max: int) -> None:
        """Задает границы движения."""
        self.max_x = x_max
        self.max_y = y_max

    def update(self, key: str, fg_layer: list["Sprite"]) -> None:
        """Теперь принимает список всех спрайтов."""
        return

    def move(self, delta_x: int, delta_y: int, fg_layer: list["Sprite"]) -> None:
        """Движение с учетом всех объектов в fg_layer."""
        new_x = self.x + delta_x
        new_y = self.y + delta_y

        if self.is_offscreen(new_x, new_y):
            return

        if self.is_colliding_obstacle(new_x, new_y, fg_layer):
            return

        self.x, self.y = new_x, new_y

    def is_colliding_obstacle(
            self, x: int, y: int, fg_layer: list["Sprite"],
    ) -> bool:
        """Коллизии с препятствиями."""
        for sprite in fg_layer:
            if (
                isinstance(sprite, Obstacle)
                and sprite.x == x
                and sprite.y == y
            ):
                return True
        return False

    def is_offscreen(self, x: int, y: int) -> bool:
        """Проверка выхода за пределы поля."""
        return (
            x < self.min_x or x > self.max_x
            or
            y < self.min_y or y > self.max_y
        )


class Player(Sprite):
    """Игрок с управлением клавишами."""

    def __init__(self, x: int, y: int) -> None:
        """Инициализирует спрайт."""
        super().__init__(x, y)
        self.img = "@"
        self.color = "green"

    def update(self, key: str, fg_layer: list[Sprite]) -> None:
        """Реакция на клавиши – движение."""
        super().update(key, fg_layer)
        dx, dy = 0, 0
        if key == config.CONTROLS["up"]:
            dy = -1
        elif key == config.CONTROLS["down"]:
            dy = 1
        elif key == config.CONTROLS["left"]:
            dx = -1
        elif key == config.CONTROLS["right"]:
            dx = 1

        if dx != 0 or dy != 0:
            self.move(dx, dy, fg_layer)


class Obstacle(Sprite):
    """Непроходимое препятствие."""

    def __init__(self, x: int, y: int) -> None:
        """Инициализирует препятствие."""
        super().__init__(x, y)
        self.img = "#"
        self.color = "red"


class Collectable(Sprite):
    """Подбираемый предмет."""

    def __init__(self, x: int, y: int) -> None:
        """Инициализирует предмет."""
        super().__init__(x, y)
        self.img = "$"
        self.color = "yellow"


class Npc(Sprite):
    """Непись."""

    def __init__(self, x: int, y: int) -> None:
        """Инициализирует спрайт."""
        super().__init__(x, y)
        self.img = "a"
        self.color = "blue"
        self.speed = 1

    def update(self, key: str, fg_layer: list[Sprite]) -> None:
        """Движение из стороны в сторону."""
        super().update(key, fg_layer)

        if self.speed == 0:
            return

        new_x = self.x + self.speed
        new_y = self.y

        if self.is_offscreen(new_x, new_y):
            self.speed *= -1
            new_x = self.x + self.speed

        if self.is_colliding_obstacle(new_x, new_y, fg_layer):
            self.speed *= -1
            new_x = self.x + self.speed

        self.x = new_x
        self.y = new_y
