"""Модуль импорта компонентов игры."""

from .game import Game
from .sprite import (
    Coin,
    Collectable,
    Door,
    Fence,
    Npc,
    Obstacle,
    Player,
    Sprite,
    Wall,
)

__all__ = [
    "Coin",
    "Collectable",
    "Door",
    "Fence",
    "Game",
    "Npc",
    "Obstacle",
    "Player",
    "Sprite",
    "Wall",
]
