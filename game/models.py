"""Общие структуры данных для обмена между модулями."""

from dataclasses import dataclass


@dataclass
class FrameData:
    """Стандартизированные данные: игра → рендер."""

    stats_lines: list[str]
    hints_lines: list[str]
    map_matrix: list[list[tuple[str, str, str]]]  # img, цвет, фон
    legend: list[str]
    log_lines: list[str]


@dataclass
class Event:
    """Событие игры: игра → рендер (или звуковая система)."""

    message: str | None = None
    sound: str | None = None
