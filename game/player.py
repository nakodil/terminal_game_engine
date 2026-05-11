"""Vодуль игрока."""

import config

from .sprite import Sprite


class Player(Sprite):
    """Игрок с управлением клавишами."""

    def __init__(self, x: int, y: int) -> None:
        """Инициализирует спрайт."""
        super().__init__(x, y)
        self.img = "@"
        self.color = "green"
        self.name = "Вася Питонов"

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
