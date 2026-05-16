"""Модуль импорта спрайтов."""

from .collectable import Coin, Collectable
from .interactive import Door
from .npc import Anakondova, Gadukin
from .obstacle import Fence, Obstacle, Wall
from .player import Player
from .sprite import Sprite

__all__ = [
    "Anakondova",
    "Coin",
    "Collectable",
    "Door",
    "Fence",
    "Gadukin",
    "Obstacle",
    "Player",
    "Sprite",
    "Wall",
]
