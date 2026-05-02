"""Модуль игры."""

from pathlib import Path

import config

from .sprite import Collectable, Npc, Obstacle, Player, Sprite

SHADES = {
    "0%": " ",
    "25%": "░",
    "50%": "▒",
    "75%": "▓",
    "100%": "█",
}


class Game:
    """Игровые объекты (спрайты) и логика."""

    def __init__(self) -> None:
        """Инициализация."""
        self.mapping = {
            "@": Player,
            "a": Npc,
            "#": Obstacle,
            "$": Collectable,
        }
        self.bg_layer: list[list[str]] = []
        self.fg_layer: list[Sprite] = []
        self.width = 0
        self.height = 0
        self.hints = [""]
        self.messages = [""]

    def _get_world_from_txt(self, filename: str) -> list:
        """Читает мир из TXT файла."""
        world_file_path = config.GAME_DIR / filename
        try:
            with Path.open(world_file_path, mode="r", encoding="utf-8") as world_file:
                data = world_file.readlines()
        except FileNotFoundError:
            return []
        return data

    def _set_world(self) -> None:
        """Создает слои игрового мира.

        TODO: Одинаковое количество колонн в рядах!
        """
        data = self._get_world_from_txt("world.txt")
        self.height = len(data)
        self.width = max(len(row.strip()) for row in data) if data else 0

        self.bg_layer = [
            [SHADES["25%"] for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self.fg_layer = []

        player = None
        for row_idx, row in enumerate(data):
            for col_idx, char in enumerate(row.strip()):
                sprite_class = self.mapping.get(char)
                if sprite_class:
                    new_sprite = sprite_class(col_idx, row_idx)
                    if sprite_class == Player:
                        player = new_sprite
                    self.fg_layer.append(new_sprite)
        if player:
            self.fg_layer.remove(player)
            self.fg_layer.append(player)  # игрок всегда на переднем плане

    def setup(self) -> None:
        """Исходное состояние."""
        self.bg_layer = []
        self.fg_layer = []
        self.width = 0
        self.height = 0
        self._set_world()
        self._setup_sprites()  # спрайты получают раницы движения
        self.hints = config.HINTS
        self.messages = ["игра началась"]

    def _setup_sprites(self) -> None:
        """Ограничивает координаты движения спрайтов."""
        for sprite in self.fg_layer:
            sprite.setup(self.width - 1, self.height - 1)

    def update(self, key: str) -> None:
        """Обновление спрайтов."""
        for sprite in self.fg_layer:
            sprite.update(key, self.fg_layer)

    def exit(self) -> None:
        """Выход из игры."""
