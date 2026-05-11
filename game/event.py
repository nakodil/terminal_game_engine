"""Модуль событий."""

from dataclasses import dataclass


@dataclass
class Event:
    """Событие игры."""

    message: str | None = None
    sound: str | None = None
