"""Модуль движка."""

import time

import config
from game import Game

from .input import InputHandler
from .render import Renderer
from .sound import SoundManager


class Engine:
    """Движок - фасад к системам.

    Системы:
    рендер,
    звук,
    ввод с клавиатуры,
    игра.
    """

    def __init__(self, game: Game) -> None:
        """Инициализация."""
        self.fps_max = 60
        self.render_system = Renderer()
        self.input_system = InputHandler()
        self.sound_system = SoundManager()
        self.game = game
        self.is_running = False
        self.setup()
        self.mainloop()

    def setup(self) -> None:
        """Возвращает все системы в исходное состояние."""
        self.render_system.setup()
        self.input_system.setup()
        self.sound_system.setup()
        self.game.setup()
        self.is_running = True

        # сначала нарисуем первый кадр, потом будем ждать клавишу
        self.render_system.update(
            self.game.bg_layer,
            self.game.fg_layer,
            self.game.hints,
            self.game.messages,
        )

    def update(self) -> None:
        """Такт главного цикла."""
        self.input_system.update()
        key_pressed = self.input_system.get_key_pressed()

        if not key_pressed:
            return

        self.on_key(key_pressed)
        self.game.update(key_pressed)

        self.sound_system.update()

        self.render_system.update(
            self.game.bg_layer,
            self.game.fg_layer,
            self.game.hints,
            self.game.messages,
        )

    def on_key(self, key: str) -> None:
        """Выход клавишей Q."""
        if key == config.CONTROLS["exit"]:
            self.is_running = False

    def mainloop(self) -> None:
        """Главный цикл."""
        while self.is_running:
            self.update()
            time.sleep(1 / self.fps_max)  # разгружаем процессор
        self.exit()

    def exit(self) -> None:
        """Выход: завершение работы систем."""
        self.render_system.exit()
        self.input_system.exit()
        self.sound_system.exit()
        self.game.exit()
