"""Модуль вывода на экран."""

import os


class Renderer:
    """Система рендера для терминала."""

    def __init__(self) -> None:
        """Инициализирует систему рендера."""
        self.show_cursor_char = "\033[?25h"
        self.hide_cursor_char = "\033[?25l"
        self.reset_cursor_char = "\033[H"
        self.colors = {
            "black":   "\033[30m",
            "red":     "\033[31m",
            "green":   "\033[32m",
            "yellow":  "\033[33m",
            "blue":    "\033[34m",
            "magenta": "\033[35m",
            "cyan":    "\033[36m",
            "white":   "\033[37m",
            "reset":   "\033[0m",
        }
        self.layout = {
            "карта": 51,
            "история": 30,
            "игрок": 30,
        }

    def setup(self) -> None:
        """Подготавливает консоль к рендеру."""
        os.system("cls" if os.name == "nt" else "clear")

    def update(self, render_data: tuple) -> None:
        """Запускает отрисовку полученных из игры данных (контента виджетов)."""
        self.render(render_data)

    def _get_map_rows_formatted(self, data: list) -> list[str]:
        """Возвращает ряды карты, наполненные цветными символами."""
        reset_color = self.colors["reset"]
        fallback_color = self.colors["red"]
        return [
            "".join(
                f"{self.colors.get(color, fallback_color)}"
                f"{char}"
                f"{reset_color}"
                for char, color in row
            )
            for row in data
        ]

    def _get_textbox_rows_formatted(
            self,
            data: list,
            width: int,
            height: int,
    ) -> list[str]:
        """Возвращает ряды текста."""
        rows = [str(line)[:width].ljust(width) for line in data[:height]]
        # Добиваем пустотой до нужной высоты
        return rows + [" " * width] * (height - len(rows))

    def render(self, widgets_content: tuple[list]) -> None:
        """Отрисовка в терминале."""
        all_rows = []
        height = len(widgets_content[0])  # все виджеты высотой с карту
        for widget_idx, widget_data in enumerate(self.layout.items()):
            title = widget_data[0].upper()
            width = widget_data[1]
            data = widgets_content[widget_idx]
            if widget_idx == 0:
                widget_rows = self._get_map_rows_formatted(data)
            else:
                widget_rows = self._get_textbox_rows_formatted(data, width, height)
            widget_rows_framed = self._add_frame(widget_rows, title, width)
            all_rows.append(widget_rows_framed)

        all_rows_formatted = ["".join(parts) for parts in zip(*all_rows, strict=True)]
        full_frame = "\n".join(all_rows_formatted)
        print(f"{self.reset_cursor_char}{self.hide_cursor_char}{full_frame}")

    def _add_frame(self, rows: list[str], title: str, width: int) -> list[str]:
        """Оборачивает список строк в рамку."""
        return [
            f"┌{title.center(width, '─')}┐",
            *[f"│{line}│" for line in rows],
            f"└{'─' * width}┘",
        ]

    def exit(self) -> None:
        """Восстанавливает терминал."""
        print(self.show_cursor_char)
