"""Модуль импорта компонентов игры."""

from .collectable import Coin, Collectable
from .event import Event
from .game import Game
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
    "Event",
    "Fence",
    "Gadukin",
    "Game",
    "Obstacle",
    "Player",
    "Sprite",
    "Wall",
]
