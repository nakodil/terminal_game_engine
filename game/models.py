"""Общие структуры данных для обмена между модулями."""

from dataclasses import dataclass


@dataclass
class FrameData:
    """Стандартизированные данные: игра → рендер."""

    left_panel_lines: list[str]
    center_matrix: list[list[tuple[str, str]]]
    right_panel_lines: list[str]


@dataclass
class Event:
    """Событие игры."""

    message: str | None = None
    sound: str | None = None
