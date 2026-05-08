"""Модуль импорта компонентов ядра."""

from .engine import Engine
from .event import Event
from .input import InputHandler
from .render import Renderer
from .sound import SoundManager

__all__ = [
    "Engine",
    "Event",
    "InputHandler",
    "Renderer",
    "SoundManager",
]
