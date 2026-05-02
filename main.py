"""Точка входа."""

from core import Engine
from game import Game

if __name__ == "__main__":
    game = Game()
    engine = Engine(game)
