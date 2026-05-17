"""Модуль виджета."""

from abc import ABC, abstractmethod
from typing import Final


class Widget(ABC):
    """Базовый контракт для любого элемента интерфейса внутри панели."""

    @property
    def fixed_height(self) -> int | None:
        """Возвращает фиксированную высоту виджета в строках.

        Если возвращает None, виджет считается 'резиновым' (Flex)
        и претендует на распределение оставшегося пространства.
        """
        return None

    @abstractmethod
    def render(self, width: int, height: int) -> list[str]:
        """Генерирует текстовый контент виджета под заданные габариты."""



class MatrixWidget(Widget):
    """Специализированный виджет для разбора и окрашивания игровой карты."""

    def __init__(
        self,
        matrix: list[list[tuple[str, str, str]]],
        colors_dict: dict[str, str],
    ) -> None:
        """Инициализирует виджет матрицей карты и таблицей ANSI-цветов."""
        self.matrix: list[list[tuple[str, str, str]]] = matrix
        self.colors: dict[str, str] = colors_dict
        self.reset: Final[str] = "\033[0m"

    @property
    def fixed_height(self) -> int | None:
        """Высота виджета жестко привязана к числу строк матрицы карты."""
        return len(self.matrix)

    def render(self, width: int, height: int) -> list[str]:
        """Генерирует цветные строки карты, дополняя пустоты пробелами."""
        rendered_lines: list[str] = []

        for y in range(height):
            if y >= len(self.matrix):
                rendered_lines.append(" " * width)
                continue

            line_buffer: list[str] = []
            row = self.matrix[y]

            for x in range(width):
                if x >= len(row):
                    line_buffer.append(" ")
                    continue

                char, fg, bg = row[x]
                fg_ansi = self.colors.get(fg, "")
                bg_ansi = self.colors.get(bg, "")
                line_buffer.append(f"{fg_ansi}{bg_ansi}{char}{self.reset}")

            rendered_lines.append("".join(line_buffer))

        return rendered_lines


class TextLinesWidget(Widget):
    """Универсальный виджет для отображения списков строк (логов, статов)."""

    def __init__(
        self,
        lines: list[str],
        is_fixed: bool = False,
        fixed_h: int | None = None,
    ) -> None:
        """Инициализирует текстовый виджет с возможностью фиксации высоты."""
        self._lines: list[str] = lines
        self._is_fixed: bool = is_fixed
        self._fixed_h: int | None = fixed_h

    @property
    def fixed_height(self) -> int | None:
        """Возвращает fixed_h, если флаг фиксации активен."""
        return self._fixed_h if self._is_fixed else None

    def render(self, width: int, height: int) -> list[str]:
        """Возвращает ровный текстовый блок, обрезанный под ширину панели."""
        rendered_lines: list[str] = []
        for i in range(height):
            if i < len(self._lines):
                rendered_lines.append(self._lines[i][:width].ljust(width))
            else:
                rendered_lines.append(" " * width)
        return rendered_lines
