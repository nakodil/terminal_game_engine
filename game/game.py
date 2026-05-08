"""Модуль игры."""

from pathlib import Path

import config
from core.event import Event

from .sprite import Coin, Door, Fence, Npc, Player, Sprite, Wall

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
        self.sprites_img_mapping = {
            "D": Door,
            "@": Player,
            "a": Npc,
            "█": Wall,
            "#": Fence,
            "●": Coin,
        }
        self.map: list[list[str]] = []
        self.sprites: list[Sprite] = []
        self.player: Player | None = None
        self.events: list[Event] = []
        self.messages: list[str] = []

    def _set_world(self) -> None:
        """Создает мир.

        Загружает ряды игрового мира (списки строк) из текстового файла;
        Определяет размеры игрвого мира;
        Создает карту;
        Создает спрайты.
        TODO: Проверить на одинаковое количество колонн в рядах!
        """
        world_rows = self._get_world_from_txt("world.txt")
        world_width = max(len(row.strip()) for row in world_rows) if world_rows else 0
        world_height = len(world_rows)

        self.map = self._get_map(world_width, world_height)

        self.sprites = self._get_sprites(world_rows)
        self._setup_sprites(world_width, world_height)

    def _get_world_from_txt(self, filename: str) -> list[str]:
        """Читает мир из TXT файла, возвращает ряды мира."""
        world_file_path = config.GAME_DIR / filename
        try:
            with Path.open(world_file_path, mode="r", encoding="utf-8") as world_file:
                rows = world_file.readlines()
        except FileNotFoundError:
            return []
        return rows

    def _get_map(self, width: int, height: int) -> list[list[str]]:
        """Возвращает двухмерную карту заполненную фоновой текстурой."""
        return [
            [SHADES["25%"] for _ in range(width)]
            for _ in range(height)
        ]

    def _get_sprites(self, rows: list[str]) -> list[Sprite]:
        """Создает спрайты - список игровых объектов."""
        sprites = []
        player = None
        for row_idx, row in enumerate(rows):
            for col_idx, char in enumerate(row.strip()):
                sprite_class = self.sprites_img_mapping.get(char)
                if sprite_class:
                    new_sprite = sprite_class(col_idx, row_idx)
                    if sprite_class == Player:
                        player = new_sprite
                        continue
                    sprites.append(new_sprite)
        if player:
            sprites.append(player)  # игрок всегда на переднем плане
            self.player = player
        return sprites

    def get_render_data(self) -> tuple:
        """Отдает данные для рендера.

        Карта;
        Сообщения;
        Статы игрока.
        """
        return (
            self.get_frame_matrix(),
            self.messages,
            str(self.player).split("; "),
        )

    def setup(self) -> None:
        """Исходное состояние."""
        self.map = []
        self.sprites = []
        self.player = None
        self._set_world()
        self.events = []
        self.messages = ["игра началась"]

    def _setup_sprites(self, world_width: int, world_height: int) -> None:
        """Ограничивает координаты движения спрайтов."""
        for sprite in self.sprites:
            sprite.setup(world_width - 1, world_height - 1)

    def get_frame_matrix(self) -> list[list[tuple[str, str]]]:
        """Собирает кадр.

        Примитив - кортеж строк (символ, цвет).
        Доступ к примитиву: кадр[idx_ряда][idx_колонны].

        1. Заполняет весь кадр примитивами фона;
        2. Заменяет нужные ячейки кадра примитивами спрайтов;
        3. Возвращает кадр.
        """
        bg_color = "white"
        frame = [
            [(char, bg_color) for char in row]
            for row in self.map
        ]

        for sprite in self.sprites:
            if sprite.is_visible:
                frame[sprite.y][sprite.x] = (sprite.img, sprite.color)

        return frame

    def _check_interactions(self) -> None:
        """Обработка взаимодействий игрока и спрайтов."""
        if not self.player:
            return

        for sprite in self.sprites[:]:
            if sprite is self.player:
                continue

            if (
                sprite.x == self.player.x
                and sprite.y == self.player.y
                and isinstance(sprite, Coin)
            ):
                self.sprites.remove(sprite)
                self.player.coins += 1  # Нет интерфейса!
                event = Event(
                    message=f"{self.player.name} подобрал {sprite.name}",
                    sound="collect",
                    )
                self.events.append(event)

    def update(self, key: str) -> None:
        """Обновление спрайтов."""
        for sprite in self.sprites:
            moved = sprite.update(key, self.sprites)
            if sprite is self.player and moved:
                self.events.append(Event(sound="walk"))
        self._check_interactions()

    def exit(self) -> None:
        """Выход из игры."""
