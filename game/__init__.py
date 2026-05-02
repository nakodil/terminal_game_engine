"""Модуль импорта компонентов игры."""

from .game import Game
from .sprite import Collectable, Npc, Obstacle, Player, Sprite

__all__ = [
    "Collectable",
    "Game",
    "Npc",
    "Obstacle",
    "Player",
    "Sprite",
]
