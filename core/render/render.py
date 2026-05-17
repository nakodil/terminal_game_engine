"""Модуль рендера."""

from typing import Final

from game.models import FrameData

from .panel import Panel
from .screen import Screen
from .widget import MatrixWidget, TextLinesWidget


class Renderer:
    """Главный координатор отрисовки интерфейса."""

    def __init__(self) -> None:
        """Инициализирует конфигурацию экрана, отступов и цветов."""
        self.screen: Screen = Screen()
        self.padding_char: Final[str] = " "
        self.left_width: Final[int] = 35

        self.colors_config: Final[dict[str, str]] = {
            "black": "\033[30m",
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "magenta": "\033[35m",
            "cyan": "\033[36m",
            "white": "\033[37m",

            "bg_black": "\033[40m",
            "bg_red": "\033[41m",
            "bg_green": "\033[42m",
            "bg_yellow": "\033[43m",
            "bg_blue": "\033[44m",
            "bg_magenta": "\033[45m",
            "bg_cyan": "\033[46m",
            "bg_white": "\033[47m",
        }

    def setup(self) -> None:
        """Подготавливает низкоуровневый экран к отрисовке."""
        self.screen.setup()

    def render(self, frame_data: FrameData, padding: int = 1) -> None:
        """Формирует и выводит кадр на основе текущих размеров терминала."""
        term_w, term_h = self.screen.get_terminal_size()

        # 1. Автоматический расчет ширины средней панели по матрице карты
        map_internal_w = (
            max(len(row) for row in frame_data.map_matrix)
            if frame_data.map_matrix
            else 0
        )
        center_width = map_internal_w + 2

        # 2. Определение доступного места для правой панели
        total_padding_w = padding * 2
        used_width = self.left_width + center_width + total_padding_w
        right_width = term_w - used_width

        # Контроль критического сжатия экрана
        min_right_width = 15
        if right_width < min_right_width:
            msg = (
                f"{self.screen.cursor_reset}Ширина окна мала! Слишком большая "
                f"карта или узкое окно. Требуется минимум: "
                f"{used_width + min_right_width}, сейчас: {term_w}"
            )
            print(msg)
            return

        # 3. Фабрикация и наполнение панелей виджетами
        p_left = Panel(width=self.left_width)
        stats_h = len(frame_data.stats_lines)
        stats_widget = TextLinesWidget(
            frame_data.stats_lines,
            is_fixed=True,
            fixed_h=stats_h,
        )
        p_left.add_widget(stats_widget)
        p_left.add_widget(TextLinesWidget(frame_data.hints_lines, is_fixed=False))

        p_center = Panel(width=center_width)
        map_widget = MatrixWidget(frame_data.map_matrix, self.colors_config)
        p_center.add_widget(map_widget)
        legend_widget = TextLinesWidget(frame_data.legend, is_fixed=False)
        p_center.add_widget(legend_widget)

        p_right = Panel(width=right_width)
        log_widget = TextLinesWidget(frame_data.log_lines, is_fixed=False)
        p_right.add_widget(log_widget)

        # 4. Сборка столбцов и отрисовка через Screen
        panels = [p_left, p_center, p_right]
        columns_to_draw: list[list[str]] = []
        pad_space = self.padding_char * padding

        for idx, panel in enumerate(panels):
            columns_to_draw.append(panel.render(height=term_h))
            if idx < len(panels) - 1:
                columns_to_draw.append([pad_space for _ in range(term_h)])

        self.screen.draw(columns_to_draw)

    def exit(self) -> None:
        """Восстанавливает стандартные параметры терминала."""
        self.screen.exit()
