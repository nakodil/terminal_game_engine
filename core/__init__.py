"""Модуль импорта компонентов ядра."""

from .engine import Engine
from .input import InputHandler
from .render import Renderer
from .sound import SoundManager

__all__ = [
    "Engine",
    "InputHandler",
    "Renderer",
    "SoundManager",
]
