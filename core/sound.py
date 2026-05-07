"""Модуль звука (Windows, winsound)."""

import winsound

import config


class SoundManager:
    """Менеджер звуков."""

    def __init__(self) -> None:
        """Инициализирует менеджер со всеми звуками из папки."""
        self.sounds: dict[str, str] = {}

        if not config.SOUND_DIR.exists():
            return

        for file_path in config.SOUND_DIR.glob("*.wav"):
            self._load(file_path.stem, file_path.name)

    def setup(self) -> None:
        """Исходное состояние."""
        self.stop()

    def update(self) -> None:
        """Обновление."""

    def _load(self, sound_name: str, file_name: str) -> None:
        """Регистрирует звук по имени."""
        self.sounds[sound_name] = str(config.SOUND_DIR / file_name)

    def play(self, name: str) -> None:
        """Проигрывает звук (асинхронно)."""
        path = self.sounds.get(name, None)
        if not path:
            return

        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)

    def stop(self) -> None:
        """Останавливает текущий звук."""
        winsound.PlaySound(None, winsound.SND_PURGE)

    def exit(self) -> None:
        """Останавливает все звуки."""
