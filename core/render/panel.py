"""Модуль панели."""

from typing import Final

from .widget import Widget


class Panel:
    """Вертикальный контейнер с декоративной рамкой.

    Автоматически рисует границы вокруг себя и стыки '├─┤' между виджетами.
    """

    def __init__(self, width: int) -> None:
        """Инициализирует панель заданной ширины."""
        self.width: int = width
        self.border_size: int = 2
        self.widgets: list[Widget] = []

    def add_widget(self, widget: Widget) -> None:
        """Добавляет виджет в вертикальную стопку панели."""
        self.widgets.append(widget)

    def _allocate_heights(self, total_height: int) -> list[int]:
        """Вычисляет и распределяет доступную высоту между виджетами."""
        total_separators = max(0, len(self.widgets) - 1)
        fixed_h = sum(
            w.fixed_height
            for w in self.widgets
            if w.fixed_height is not None
        )
        dyn_widgets = [w for w in self.widgets if w.fixed_height is None]

        avail_dyn = max(0, total_height - total_separators - fixed_h)
        dyn_quota = avail_dyn // len(dyn_widgets) if dyn_widgets else 0
        unalloc_dyn = avail_dyn

        heights: list[int] = []
        current_y = 0

        for widget in self.widgets:
            # Если высота панели исчерпана
            if current_y >= total_height:
                heights.append(0)
                continue

            # Резервируем место под разделитель (кроме первого виджета)
            if heights:
                current_y += 1
                if current_y >= total_height:
                    heights.append(0)
                    continue

            # Вычисляем запрашиваемую высоту виджета
            if widget.fixed_height is not None:
                requested_h = widget.fixed_height
            elif widget is dyn_widgets[-1]:
                requested_h = unalloc_dyn
                unalloc_dyn = 0
            else:
                requested_h = dyn_quota
                unalloc_dyn -= requested_h

            # Обрезаем под остаток места на экране
            allocated_h = min(requested_h, total_height - current_y)
            heights.append(max(0, allocated_h))
            current_y += allocated_h

        return heights

    def _format_widget(self, widget: Widget, width: int, height: int) -> list[str]:
        """Отрендерить строки виджета и обернуть их в боковые рамки '│'."""
        formatted: list[str] = []
        raw_lines = widget.render(width=width, height=height)

        for i in range(height):
            if i < len(raw_lines):
                line = raw_lines[i]
                # ljust ломает цветной вывод, применяем только к обычному тексту
                if "\033" not in line:
                    line = line[:width].ljust(width)
            else:
                line = " " * width
            formatted.append(f"│{line}│")

        return formatted

    def _build_frame(self, content: list[str], int_w: int, int_h: int) -> list[str]:
        """Собирает финальный блок с верхней и нижней рамкой, заполняя пустоту."""
        padding = [f"│{' ' * int_w}│" for _ in range(int_h - len(content))]
        return [
            f"┌{'─' * int_w}┐",
            *content,
            *padding,
            f"└{'─' * int_w}┘",
        ]

    def render(self, height: int) -> list[str]:
        """Отрендерить панель в рамке на заданную высоту терминала."""
        if height < self.border_size or self.width < self.border_size:
            return [" " * self.width for _ in range(height)]

        int_w: Final[int] = self.width - self.border_size
        int_h: Final[int] = height - self.border_size

        if not self.widgets:
            return self._build_frame([], int_w, int_h)[:height]

        heights = self._allocate_heights(int_h)
        content_lines: list[str] = []

        for idx, (widget, w_h) in enumerate(zip(self.widgets, heights, strict=True)):
            if len(content_lines) >= int_h:
                break

            # Интегрируем разделитель
            if idx > 0:
                content_lines.append(f"├{'─' * int_w}┤")
                if len(content_lines) >= int_h:
                    break

            # Запрашиваем рендер и добавляем отформатированные строки виджета
            if w_h > 0:
                content_lines.extend(self._format_widget(widget, int_w, w_h))

        return self._build_frame(content_lines, int_w, int_h)[:height]
