"""Модуль игры."""

from pathlib import Path

import config

from .collectable import Coin, Collectable
from .event import Event
from .interactive import Door
from .npc import Anakondova, Gadukin
from .obstacle import Fence, Wall
from .player import Player
from .sprite import Sprite

# куда бы их деть?
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
            "A": Anakondova,
            "G": Gadukin,
            "█": Wall,
            "#": Fence,
            "●": Coin,
        }
        self.world_map: list[list[str]] = []
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
        """
        world_rows = self._get_world_from_file("world.txt")

        world_width = max(len(row.strip()) for row in world_rows) if world_rows else 0
        world_height = len(world_rows)

        self.world_map = self._get_map(world_width, world_height, SHADES["25%"])

        self.sprites = self._get_sprites(world_rows)
        self._setup_sprites(world_width, world_height)

    def _get_world_from_file(self, filename: str) -> list[str]:
        """Читает мир из TXT файла, возвращает ряды мира."""
        world_file_path = config.GAME_DIR / filename
        try:
            with Path.open(world_file_path, encoding="utf-8") as world_file:
                world_rows = world_file.readlines()
        except FileNotFoundError:
            return []
        return world_rows

    def _get_map(self, width: int, height: int, img: str) -> list[list[str]]:
        """Возвращает двухмерную карту заполненную одинаковыми текстурами."""
        return [
            [img for _ in range(width)]
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
        self.world_map = []
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
            for row in self.world_map
        ]

        for sprite in self.sprites:
            if sprite.is_visible:
                frame[sprite.y][sprite.x] = (sprite.img, sprite.color)

        return frame

    def get_sprite_at(self, x: int, y: int) -> Sprite | None:
        """Возвращает спрайт по указанным координатам (кроме игрока)."""
        for sprite in self.sprites:
            if (
                sprite is not self.player
                and sprite.x == x
                and sprite.y == y
            ):
                return sprite
        return None

    def update(self, key: str) -> None:
        """Обновление состояния игры за один такт."""
        # 1. Получаем вектор движения игрока
        offset = self._get_move_offset(key)

        # 2. Если игрок нажал на движение — обрабатываем экшен
        if offset and self.player:
            self._handle_player_step(*offset)

        # 3. Обновляем все остальные спрайты
        self._update_others(key)

    def _get_move_offset(self, key: str) -> tuple[int, int] | None:
        """Превращает клавишу в вектор (dx, dy)."""
        move_map = {
            config.CONTROLS["up"]: (0, -1),
            config.CONTROLS["down"]: (0, 1),
            config.CONTROLS["left"]: (-1, 0),
            config.CONTROLS["right"]: (1, 0),
        }
        return move_map.get(key)

    def _handle_player_step(self, dx: int, dy: int) -> None:
        """Логика взаимодействия игрока с миром при попытке шага."""
        if self.player is None:
            return
        target_x = self.player.x + dx
        target_y = self.player.y + dy
        target_sprite = self.get_sprite_at(target_x, target_y)

        # Если впереди кто-то есть — взаимодействуем
        if target_sprite:
            event = target_sprite.interact(self.player)
            if event:
                self.events.append(event)

            # Если это предмет — убираем его
            if isinstance(target_sprite, Collectable):
                self.sprites.remove(target_sprite)

            # Если объект твердый — прерываем шаг
            if target_sprite.is_solid:
                return

        # Если мы здесь — путь либо пуст, либо там был нетвердый объект (монета)
        if self.player.move(dx, dy, self.sprites):
            self.events.append(Event(sound="walk"))

    def _update_others(self, key: str) -> None:
        """Обновляет логику всех спрайтов, кроме игрока."""
        for sprite in self.sprites:
            if sprite is not self.player:
                sprite.update(key, self.sprites)

    def exit(self) -> None:
        """Выход из игры."""
