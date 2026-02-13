"""Первый уровень."""

from game import config
from game.config import tilemaps
from game.screens import BaseScreen

SPAWN_POS = 5 + 1 * 32 * config.TILE_SCALING, 6 + 1 * 32 * config.TILE_SCALING


class SchoolLevelScreen(BaseScreen):
    """Первый уровень."""

    def __init__(self) -> None:
        """Инициализация класса."""
        super().__init__(SPAWN_POS, tilemaps.SCHOOL_LEVEL)
