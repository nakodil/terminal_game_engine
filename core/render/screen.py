"""Модуль экрана."""

import os
from typing import Final


class Screen:
    """Низкоуровневая работа с буфером и управляющими командами терминала."""

    def __init__(self) -> None:
        """Инициализирует управляющие ANSI-последовательности."""
        self.cursor_reset: Final[str] = "\033[H"
        self.cursor_hide: Final[str] = "\033[?25l"
        self.cursor_show: Final[str] = "\033[?25h"

    def get_terminal_size(self) -> tuple[int, int]:
        """Возвращает актуальные размеры окна терминала (ширина, высота)."""
        size = os.get_terminal_size()
        return size.columns, size.lines

    def draw(self, columns_data: list[list[str]]) -> None:
        """Склеивает вертикальные колонки панелей в единый кадр и выводит его."""
        rendered_rows = ["".join(row) for row in zip(*columns_data, strict=True)]
        full_frame = "\n".join(rendered_rows)
        print(f"{self.cursor_reset}{full_frame}", end="", flush=True)

    def setup(self) -> None:
        """Очищает экран и скрывает курсор перед стартом игры."""
        os.system("cls" if os.name == "nt" else "clear")
        print(self.cursor_hide, end="")

    def exit(self) -> None:
        """Возвращает курсор в видимое состояние при выходе."""
        print(self.cursor_show)
