"""Модуль конфигурации."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
GAME_DIR = BASE_DIR / "game"
ASSETS_DIR = GAME_DIR / "assets"
SOUND_DIR = ASSETS_DIR / "sound"

TITLE = "Игра"

CONTROLS = {
    "up": "w",
    "down": "s",
    "left": "a",
    "right": "d",
    "exit": "q",
}
