"""Модуль звука (Windows, winsound)."""

import winsound

import config


class SoundManager:
    """Менеджер звуков."""

    def __init__(self) -> None:
        """Инициализирует менеджер."""
        self.sounds: dict[str, str] = {}
        # Загрузить все звуки из assets/sound/

    def setup(self) -> None:
        """Исходное состояние."""
        # Заглушить все звуки

    def update(self) -> None:
        """Обновление."""

    def _load(self, sound_name: str, file_name: str) -> None:
        """Регистрирует звук по имени."""
        self.sounds[sound_name] = str(config.SOUND_DIR / file_name)

    def play(self, name: str) -> None:
        """Проигрывает звук (асинхронно)."""
        path = self.sounds.get(name)
        if not path:
            return

        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)

    def stop(self) -> None:
        """Останавливает текущий звук."""
        winsound.PlaySound(None, winsound.SND_PURGE)

    def exit(self) -> None:
        """Останавливает все звуки."""
