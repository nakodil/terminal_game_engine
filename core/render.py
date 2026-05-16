"""Модуль вывода на экран."""

import os

from game.models import FrameData


class Renderer:
    """Система рендера: связывает игру, экран и панели."""

    def __init__(self) -> None:
        """Инициализирует экран и настройки геометрии колонок."""
        self.screen: Screen = Screen(min_width=110)

        # Размеры КОНТЕНТА внутри панелей (рамки добавят по +2 символа к каждой)
        self.side_width: int = 30   # Левая панель (статы и подсказки)
        self.map_width: int = 51    # Центральная панель (карта)
        self.log_width: int = 35    # Минимальная ширина правой панели (логи)
        self.padding: int = 1       # Горизонтальный отступ ("воздух") между панелями

        self.colors: dict[str, str] = {
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

    def setup(self, render_data: FrameData) -> None:
        """Первичная настройка терминала и отрисовка первого кадра."""
        self.screen.setup()
        self.render(render_data)

    def update(self, render_data: FrameData) -> None:
        """Обновление текущего кадра."""
        self.render(render_data)

    def render(self, frame: FrameData) -> None:
        """Формирует и выводит кадр."""
        term_w, term_h = self.screen.get_terminal_size()

        if term_w < self.screen.min_width:
            print(f"{self.screen.cursor_reset}Ширина терминала слишком мала!")
            return

        # Высота для внутренностей панелей (учитываем место под верхнюю и нижнюю рамку)
        content_h = term_h - 2

        # --- 1. ЛЕВАЯ ПАНЕЛЬ ---
        side_panel = Panel(width=self.side_width, height=content_h)
        side_col = side_panel.format_rows(frame.left_panel_lines, has_border=True)

        # --- 2. ЦЕНТРАЛЬНАЯ ПАНЕЛЬ (Карта) ---
        map_rows_colored = self._get_map_rows_formatted(frame.center_matrix)
        map_height = len(map_rows_colored)
        map_panel = Panel(width=self.map_width, height=content_h)
        map_col = map_panel.format_rows(map_rows_colored, is_ansi=True, has_border=True)

        # --- 3. ПРАВАЯ ПАНЕЛЬ (Лог) ---
        # 3 панели по 2 символа на рамки = 6 символов уходит на декорации
        total_borders_w = 6
        dynamic_log_w = (
            term_w
            - self.side_width
            - self.map_width
            - (self.padding * 2)
            - total_borders_w
        )
        final_log_w = max(self.log_width, dynamic_log_w)

        log_panel = Panel(width=final_log_w, height=content_h)
        # Ограничиваем логи по высоте карты, чтобы они не падали ниже её края
        logs_to_render = frame.right_panel_lines[:map_height]
        log_col = log_panel.format_rows(logs_to_render, has_border=True)

        # --- 4. СБОРКА ---
        # Для разделителей рамки НЕ нужны, поэтому передаем всю высоту
        pad_panel = Panel(width=self.padding, height=term_h)
        pad_col = pad_panel.format_rows([], has_border=False)

        self.screen.draw([side_col, pad_col, map_col, pad_col, log_col])

    def _get_map_rows_formatted(self, data: list[list[tuple[str, str]]]) -> list[str]:
        """Превращает матрицу (символ, цвет) в список готовых ANSI-строк."""
        reset = self.colors["reset"]
        fallback = self.colors["red"]
        formatted_rows = []
        for row in data:
            line = "".join(
                f"{self.colors.get(color, fallback)}{char}{reset}"
                for char, color in row
            )
            formatted_rows.append(line)
        return formatted_rows

    def exit(self) -> None:
        """Восстанавливает стандартное состояние терминала."""
        self.screen.exit()


class Screen:
    """Управление низкоуровневым выводом в терминал."""

    def __init__(self, min_width: int) -> None:
        """Инициализирует экран и ANSI-коды управления курсором."""
        self.min_width = min_width
        self.cursor_reset: str = "\033[H"
        self.cursor_hide: str = "\033[?25l"
        self.cursor_show: str = "\033[?25h"

    def get_terminal_size(self) -> tuple[int, int]:
        """Возвращает текущие размеры окна терминала."""
        size = os.get_terminal_size()
        return size.columns, size.lines

    def draw(self, columns: list[list[str]]) -> None:
        """Склеивает колонки в один кадр и выводит его."""
        rendered_rows = ["".join(row) for row in zip(*columns, strict=True)]
        full_frame = "\n".join(rendered_rows)
        print(f"{self.cursor_reset}{full_frame}", end="", flush=True)

    def setup(self) -> None:
        """Очищает экран и скрывает курсор."""
        os.system("cls" if os.name == "nt" else "clear")
        print(self.cursor_hide, end="")

    def exit(self) -> None:
        """Возвращает видимость курсора."""
        print(self.cursor_show)


class Panel:
    """Вертикальная секция экрана с фиксированной шириной контента."""

    def __init__(self, width: int, height: int) -> None:
        """Инициализирует размеры контента панели."""
        self.width = width
        self.height = height

    def format_rows(
            self,
            data: list[str],
            is_ansi: bool = False,
            has_border: bool = True,
    ) -> list[str]:
        """Форматирует ряды.

        Форматирует входящие строки под размеры панели
        и добавляет рамки при необходимости.
        """
        all_rows: list[str] = []

        # 1. Форматируем и выравниваем строки контента
        for line in data:
            if is_ansi:
                # Карта: коды цвета игнорируются, при рассчете ширины
                all_rows.append(line)
            else:
                # Текст: обрезаем и дополняем пробелами до ширины контента
                all_rows.append(line[:self.width].ljust(self.width))

        # 2. Добиваем пустые строки по вертикали до высоты контента
        padding_needed = self.height - len(all_rows)
        if padding_needed > 0:
            blank_line = " " * self.width
            all_rows.extend([blank_line for _ in range(padding_needed)])

        # Строго отсекаем лишнее по высоте контента
        all_rows = all_rows[:self.height]

        # 3. Навешиваем декоративную рамку, если требуется
        if has_border:
            top_border = f"┌{'─' * self.width}┐"
            bottom_border = f"└{'─' * self.width}┘"

            # Собираем всё за один проход без единого .append()
            return [
                top_border,
                *[f"│{row}│" for row in all_rows],
                bottom_border,
            ]

        return all_rows
