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
        self.game = game
        self.input_system = InputHandler()
        self.sound_system = SoundManager()
        self.render_system = Renderer()
        self.is_running = False
        self.setup()
        self.mainloop()

    def _handle_events(self) -> None:
        """Диспетчер событий.

        1. Выбирает самое старое событие игры;
        2. Удаляет его;
        3. Отдает текст события в сообщения игры;
        4. Отдает звук системе звука.
        """
        while self.game.events:
            event = self.game.events.pop(0)
            if event.message:
                self.game.messages.append(event.message)
            if event.sound:
                self.sound_system.play(event.sound)

    def setup(self) -> None:
        """Возвращает все системы в исходное состояние."""
        self.input_system.setup()
        self.game.setup()
        self.sound_system.setup()
        render_data = self.game.get_render_data()
        self.render_system.setup(render_data)
        self.is_running = True

    def update(self) -> None:
        """Такт главного цикла.

        1. Обновляет систему ввода;
        2. Получает нажатую клавишу из системы ввода;
        3. Завершается если клавиша пустая
           - пошаговая игра: все ждут "хода" игрока;
        4. Проверяет выход по клавише q;
        5. Отдает клавишу игре;
        6. Обновляет систему звука;
        7. Получает примитивы спрайтов игры;
        8. Отдает на рендер данные игры.
        """
        self.input_system.update()
        key_pressed = self.input_system.get_key_pressed()

        if not key_pressed:
            return

        self.on_key(key_pressed)
        self.game.update(key_pressed)

        self._handle_events()

        self.sound_system.update()

        render_data = self.game.get_render_data()
        self.render_system.update(render_data)

    def on_key(self, key: str) -> None:
        """Выход клавишей q."""
        if key == config.CONTROLS["exit"]:
            self.is_running = False

    def mainloop(self) -> None:
        """Главный цикл."""
        while self.is_running:  # меняется в on_key
            self.update()
            time.sleep(1 / self.fps_max)  # разгружаем процессор
        self.exit()

    def exit(self) -> None:
        """Выход: завершение работы систем."""
        self.render_system.exit()
        self.input_system.exit()
        self.sound_system.exit()
        self.game.exit()
