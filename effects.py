"""Модуль эффектов инрового поля."""
import random


def shuffle(grid:list[list[str]]) -> None:
    """Перемешивает клетки каждого ряда, потом перемешивает все ряды."""
    for row in grid:
        random.shuffle(row)
    random.shuffle(grid)


def checker(grid:list[list[str]]) -> None:
    """Наполняет поле клетками с чередующимися шашечкой цветами."""
    chars = ("█", "░")
    for row_idx, row in enumerate(grid):
        for col_idx, _ in enumerate(row):
            grid[row_idx][col_idx] = chars[(row_idx + col_idx) % 2]



