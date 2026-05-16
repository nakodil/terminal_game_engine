"""Модуль игры."""

from pathlib import Path

import config
from game.models import Event, FrameData
from game.sprites import (
    Anakondova,
    Coin,
    Collectable,
    Door,
    Fence,
    Gadukin,
    Player,
    Sprite,
    Wall,
)

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
        sprites_classes = (Door, Player, Anakondova, Gadukin, Wall, Fence, Coin)
        self.sprites_img_mapping = {
            sprite_class.img: sprite_class
            for sprite_class in sprites_classes
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
        player: Player | None = None  # 1. Явно подсказываем тип для Pylance

        for row_idx, row in enumerate(rows):
            for col_idx, char in enumerate(row.strip()):
                sprite_class = self.sprites_img_mapping.get(char)
                if sprite_class:
                    new_sprite = sprite_class(col_idx, row_idx)
                    if isinstance(new_sprite, Player):
                        player = new_sprite
                        continue
                    sprites.append(new_sprite)

        if player:
            sprites.append(player)  # игрок всегда на переднем плане
            self.player = player

        return sprites

    def get_render_data(self) -> FrameData:
        """Отдает стандартизированные данные для рендера."""
        left_lines = [*str(self.player).split("; "), "", *self._get_all_hints()]

        # Последние сообщения сверху
        right_lines = list(reversed(self.messages))

        return FrameData(
            left_panel_lines=left_lines,
            center_matrix=self._get_frame_matrix(),
            right_panel_lines=right_lines,
        )

    def setup(self) -> None:
        """Исходное состояние."""
        self.world_map = []
        self.sprites = []
        self.player = None
        self._set_world()
        self.events = []
        self.messages = []
        if self.player:
            start_message = f"{self.player.name} пришел в Энск"
            self.messages.append(start_message)

    def _setup_sprites(self, world_width: int, world_height: int) -> None:
        """Ограничивает координаты движения спрайтов."""
        for sprite in self.sprites:
            sprite.setup(world_width - 1, world_height - 1)

    def _get_frame_matrix(self) -> list[list[tuple[str, str]]]:
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

    def _get_nearby_sprites(self) -> dict[str, Sprite]:
        """Ищет интерактивные объекты в радиусе 1 клетки."""
        if not self.player:
            return {}

        check_points = [
            (0, 0, "под ногами"),
            (0, -1, "сверху"),
            (0, 1, "снизу"),
            (-1, 0, "слева"),
            (1, 0, "справа"),
        ]

        targets = {}
        for dx, dy, label in check_points:
            target = self.get_sprite_at(self.player.x + dx, self.player.y + dy)
            # Проверяем, что это не игрок и со спрайтом можно взаимодействовать
            if (
                target
                and target is not self.player
                and target.is_interactive
            ):
                targets[label] = target

        return targets

    def _get_action_hints(self, targets: dict[str, Sprite]) -> list[str]:
        """Формирует список подсказок для игрока."""
        hints = []
        keys = ["1", "2", "3", "4", "5"]

        for i, (label, sprite) in enumerate(targets.items()):
            if i < len(keys):
                hints.append(f"[{keys[i]}] {sprite.name} ({label})")

        return hints

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
        """Обновление."""
        # 1. Сканируем окружение
        targets = self._get_nearby_sprites()

        # 2. Если нажата клавиша взаимодействия (например, '1'...'5')
        action_keys = ["1", "2", "3", "4", "5"]
        if key in action_keys:
            idx = action_keys.index(key)
            # Взаимодействие с целью
            if idx < len(targets):
                target_sprite = list(targets.values())[idx]
                self._execute_interaction(target_sprite)
                return # Завершаем ход после действия

        # 3. Обработка движения
        offset = self._get_move_offset(key)
        if offset:
            self._handle_player_step(*offset)

        self._update_others(key)

    def _get_all_hints(self) -> list[str]:
        """Собирает все доступные команды для виджета подсказок."""
        hints = [
            f"[{config.CONTROLS["up"]}] вверх",
            f"[{config.CONTROLS["down"]}] вниз",
            f"[{config.CONTROLS["left"]}] влево",
            f"[{config.CONTROLS["right"]}] вправо",
            f"[{config.CONTROLS["exit"]}] выход из игры",
        ]

        targets = self._get_nearby_sprites()
        if targets:
            hints.extend(self._get_action_hints(targets))

        return hints

    def _execute_interaction(self, target: Sprite) -> None:
        """Логика выполнения самого действия."""
        if not self.player:
            return

        event = target.interact(self.player)
        if event:
            self.events.append(event)

        if isinstance(target, Collectable):
            self.sprites.remove(target)

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
        """Логика движения."""
        if self.player is None:
            return

        target_x = self.player.x + dx
        target_y = self.player.y + dy
        target_sprite = self.get_sprite_at(target_x, target_y)

        # Если впереди твердый объект (стена, забор) — просто стоим
        if target_sprite and target_sprite.is_solid:
            return

        # Если путь свободен (или там нетвердый спрайт типа монеты) — идем
        if self.player.move(dx, dy, self.sprites):
            self.events.append(Event(sound="walk"))

    def _update_others(self, key: str) -> None:
        """Обновляет логику всех спрайтов, кроме игрока."""
        for sprite in self.sprites:
            if sprite is not self.player:
                sprite.update(key, self.sprites)

    def exit(self) -> None:
        """Выход из игры."""
