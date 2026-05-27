"""Модуль рендера."""

from typing import Final

from game.models import FrameData

from .panel import Panel
from .screen import Screen
from .widget import MatrixWidget, TextLinesWidget


class Renderer:
    """Координирует отрисовку интерфейса.

    Экран > панель > виджет
    """

    def __init__(self) -> None:
        """Инициализирует конфигурацию экрана, отступов и цветов."""
        self.screen: Screen = Screen()
        self.padding_char: Final[str] = " "
        self.left_panel_width: Final[int] = 35

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
        """Формирует и выводит кадр на основе текущих размеров терминала.

        Левая панель фиксированной ширины,
        средняя шириной с самый длинный ряд карты,
        правая - оставшееся место.

        Каждая панель окружена декоративной рамкой (+ 2 символа: слева и справа)
        """
        terminal_width, terminal_height = self.screen.get_terminal_size()

        # Ширина средней панели = самый широкий ряд карты + рамки слева и справа
        map_width = (
            max(len(row) for row in frame_data.map_matrix)
            if frame_data.map_matrix
            else 0
        )
        center_panel_width = map_width + 2

        # Ширина правой панели = вся оставшаяся от левой и средней
        total_padding_w = padding * 2
        used_width = self.left_panel_width + center_panel_width + total_padding_w
        right_panel_width = terminal_width - used_width

        # Контроль минимальной ширины правой панели
        min_right_panel_width = 15
        if right_panel_width < min_right_panel_width:
            msg = (
                f"{self.screen.cursor_reset}Ширина окна мала! Слишком большая "
                f"карта или узкое окно. Требуется минимум: "
                f"{used_width + min_right_panel_width}, сейчас: {terminal_width}"
            )
            print(msg)
            return

        # Панели
        panel_left = Panel(width=self.left_panel_width)
        panel_center = Panel(width=center_panel_width)
        panel_right = Panel(width=right_panel_width)

        # Виджет статов игрока
        stats_h = len(frame_data.stats_lines)
        stats_widget = TextLinesWidget(
            frame_data.stats_lines,
            is_fixed=True,
            fixed_h=stats_h,
        )
        panel_left.add_widget(stats_widget)

        # Виджет доступных действий
        hints_widget = TextLinesWidget(frame_data.hints_lines, is_fixed=False)
        panel_left.add_widget(hints_widget)

        # Виждет карты
        map_widget = MatrixWidget(frame_data.map_matrix, self.colors_config)
        panel_center.add_widget(map_widget)

        # Виджет легенды
        legend_widget = TextLinesWidget(frame_data.legend, is_fixed=False)
        panel_center.add_widget(legend_widget)

        # Виджет сообщений
        log_widget = TextLinesWidget(frame_data.log_lines, is_fixed=False)
        panel_right.add_widget(log_widget)

        # Сборка панелей
        panels = [panel_left, panel_center, panel_right]
        columns_to_draw: list[list[str]] = []
        pad_space = self.padding_char * padding

        for idx, panel in enumerate(panels):
            columns_to_draw.append(panel.render(height=terminal_height))
            if idx < len(panels) - 1:
                columns_to_draw.append(
                    [pad_space for _ in range(terminal_height)],
                )

        # Отрисовка панелей
        self.screen.draw(columns_to_draw)

    def exit(self) -> None:
        """Восстанавливает стандартные параметры терминала."""
        self.screen.exit()
