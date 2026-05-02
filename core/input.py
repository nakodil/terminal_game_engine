"""Модуль ввода с клавиатуры."""

import msvcrt


class InputHandler:
    """Объект для чтения ввода с клавиатуры."""

    def __init__(self) -> None:
        """Инициализирует экземпляр чтения ввода с клавиатуры."""
        self._last_key = ""

    def setup(self) -> None:
        """Задает исходное состояние."""
        self._last_key = ""

    def update(self) -> None:
        """Обновление."""
        self._last_key  = self._get_key()

    def get_key_pressed(self) -> str:
        """Возвращает последнюю нажатую клавишу."""
        return self._last_key

    def _get_key(self) -> str:
        """Возвращает нажатую клавишу строкой."""
        if msvcrt.kbhit():
            key = msvcrt.getch()
            try:
                return key.decode("utf-8")
            except UnicodeDecodeError:
                return ""
        return ""

    def exit(self) -> None:
        """Выход."""
