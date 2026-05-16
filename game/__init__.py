"""Модуль импорта компонентов игры."""

from .game import Game
from .models import Event, FrameData
from .sprites import (
    Anakondova,
    Coin,
    Collectable,
    Door,
    Fence,
    Gadukin,
    Obstacle,
    Player,
    Sprite,
    Wall,
)

__all__ = [
    "Anakondova",
    "Coin",
    "Collectable",
    "Door",
    "Event",
    "Fence",
    "FrameData",
    "Gadukin",
    "Game",
    "Obstacle",
    "Player",
    "Sprite",
    "Wall",
]
