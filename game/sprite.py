"""Модуль спрайта."""

from __future__ import annotations

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
        self.name = "дефолтный спрайт"

    def setup(self, x_max: int, y_max: int) -> None:
        """Задает границы движения."""
        self.max_x = x_max
        self.max_y = y_max

    def update(self, _: str, __: list[Sprite]) -> None:
        """Теперь принимает список всех спрайтов."""
        return

    def move(self, delta_x: int, delta_y: int, sprites: list[Sprite]) -> None:
        """Движение.

        Вычисляет новые координаты;
        Проверяет выход за пределы "экрана";
        Проверяет столкновения с препятствиями;
        Задает спрайту новые координаты.
        """
        new_x = self.x + delta_x
        new_y = self.y + delta_y

        if self.is_offscreen(new_x, new_y):
            return

        if self.is_colliding_obstacle(new_x, new_y, sprites):
            return

        self.x, self.y = new_x, new_y

    def is_colliding_obstacle(
            self, x: int, y: int, sprites: list[Sprite],
    ) -> bool:
        """Коллизии с препятствиями."""
        for sprite in sprites:
            if (
                isinstance(sprite, Obstacle)
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


class Player(Sprite):
    """Игрок с управлением клавишами."""

    def __init__(self, x: int, y: int) -> None:
        """Инициализирует спрайт."""
        super().__init__(x, y)
        self.img = "@"
        self.color = "green"
        self.name = "Вася Питонов"
        self.hp_max = 100
        self.hp = self.hp_max
        self.coins = 0

    def __str__(self) -> str:
        """Статы."""
        up = config.CONTROLS["up"]
        down = config.CONTROLS["down"]
        left = config.CONTROLS["left"]
        right = config.CONTROLS["right"]
        return (
            f"{self.name}; "
            f"здоровье: {self.hp}/{self.hp_max}; "
            f"монеты: {self.coins}; "
            f"управление: {up}{down}{left}{right}"
        )

    def update(self, key: str, sprites: list[Sprite]) -> None:
        """Реакция на клавиши – движение."""
        super().update(key, sprites)
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
            self.move(dx, dy, sprites)


class Obstacle(Sprite, ABC):
    """Непроходимое препятствие."""

    @abstractmethod
    def __init__(self, x: int, y: int) -> None:
        """Инициализирует препятствие."""
        super().__init__(x, y)


class Wall(Obstacle):
    """Стена."""

    def __init__(self, x: int, y: int) -> None:
        """Инициализация."""
        super().__init__(x, y)
        self.img = "█"
        self.color = "red"


class Fence(Obstacle):
    """Забор."""

    def __init__(self, x: int, y: int) -> None:
        """Инициализация."""
        super().__init__(x, y)
        self.img = "#"
        self.color = "red"


class Door(Sprite):
    """Дверь."""

    def __init__(self, x: int, y: int) -> None:
        """Инициализирует дверь."""
        super().__init__(x, y)
        self.img = "D"
        self.color = "magenta"


class Collectable(Sprite):
    """Подбираемый предмет."""

    @abstractmethod
    def __init__(self, x: int, y: int) -> None:
        """Инициализирует предмет."""
        super().__init__(x, y)
        self.name = "подбираемый предмет"
        self.img = "$"
        self.color = "white"


class Coin(Collectable):
    """Монета."""

    def __init__(self, x: int, y: int) -> None:
        """Инициализирует монету."""
        super().__init__(x, y)
        self.name = "монета"
        self.img = "●"
        self.color = "yellow"
        self.value = 1


class Npc(Sprite):
    """Непись."""

    def __init__(self, x: int, y: int) -> None:
        """Инициализирует спрайт."""
        super().__init__(x, y)
        self.img = "a"
        self.color = "blue"
        self.speed = 1

    def update(self, key: str, sprites: list[Sprite]) -> None:
        """Движение из стороны в сторону."""
        super().update(key, sprites)

        if self.speed == 0:
            return

        new_x = self.x + self.speed
        new_y = self.y

        if self.is_offscreen(new_x, new_y):
            self.speed *= -1
            new_x = self.x + self.speed

        if self.is_colliding_obstacle(new_x, new_y, sprites):
            self.speed *= -1
            new_x = self.x + self.speed

        self.x = new_x
        self.y = new_y
