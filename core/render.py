"""Модуль вывода на экран."""

import os

import config
from game import Sprite


class Renderer:
    """Объект для вывода на экран.

    Неблокирующий неморгающий вывод в терминал:
        Перед первым кадром весь текст в терминале очищается.
        Кадр в виде строки собирается из игрового поля.
        Курсор консоли помещается в верхний левый угол (0, 0)
        с помощью последовательности ANSI.
        Следующий кадр выводится поверх предыдущего за один вызов print().
        Частота отрисовки сделана не ожиданием программы, а накоплением delta_time
    """

    def __init__(self) -> None:
        """Инициализирует экземпляр для вывода на экран."""
        self.show_cursor_char = "\033[?25h"
        self.hide_cursor_char = "\033[?25l"
        self.reset_cursor_char = "\033[H"
        self.colors_mapping = {
            "black":   "\033[30m",
            "red":     "\033[31m",
            "green":   "\033[32m",
            "yellow":  "\033[33m",
            "blue":    "\033[34m",
            "magenta": "\033[35m",
            "cyan":    "\033[36m",
            "white":   "\033[37m",
            "reset": "\033[0m",
        }

    def _clear(self) -> None:
        """Очищает терминал."""
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def setup(self) -> None:
        """Подготавливает консоль к рендеру."""
        os.system("cls")

    def update(
            self,
            bg_layer: list[list[str]],
            fg_layer: list[Sprite],
            hints: list[str],
            messages: list[str],
    ) -> None:
        """Обновление."""
        self.render(
            bg_layer,
            fg_layer,
            hints,
            messages,
        )

    def render(
            self,
            bg_layer: list[list[str]],
            fg_layer: list[Sprite],
            hints: list[str],
            messages: list[str],
        ) -> None:
        """Собирает и выводит кадр в терминал."""
        if not bg_layer:
            err_no_bg = "Нет фонового слоя."
            raise RuntimeError(err_no_bg)
        if not fg_layer:
            err_no_fg = "Нет слоя спрайтов."
            raise RuntimeError(err_no_fg)

        bg_layer_copy = [row[:] for row in bg_layer]

        for sprite in fg_layer:
            colored_img = (
                self.colors_mapping[sprite.color]
                + sprite.img
                + self.colors_mapping["reset"]
            )
            bg_layer_copy[sprite.y][sprite.x] = colored_img

        framed_world = self._get_framed_layer(bg_layer_copy, config.TITLE)

        if hints:
            framed_world += ", ".join(hints)

        if messages:
            framed_world += "\n" + "\n".join(map(str, messages)) + "\n"

        full_frame = (
            self.reset_cursor_char
            + self.hide_cursor_char
            + framed_world
        )
        print(full_frame)

    def _get_framed_layer(self, layer: list[list[str]], title: str) -> str:
        """Возвращает слой строкой с рамкой вокруг."""
        framed_world = "┌" + title.center(len(layer[0]), "─") + "┐\n"
        for row in layer:
            framed_world += "│" + "".join(row) + "│\n"
        framed_world += "└" + "─" * len(layer[0]) + "┘\n"
        return framed_world

    def exit(self) -> None:
        """Возвращает видимость курсора."""
        print(self.show_cursor_char)
