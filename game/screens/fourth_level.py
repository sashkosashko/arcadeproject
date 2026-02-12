from random import randint

import arcade

from game import config
from game.change_screen import change_screen
from game.components import Dialog
from game.config import sounds, textures, tilemaps
from game.screens import BaseScreen

SPAWN_POS = 5 + 1 * 32 * config.TILE_SCALING, 6 + 1 * 32 * config.TILE_SCALING


class FourthLevelScreen(BaseScreen):
    """Первый уровень."""

    def __init__(self) -> None:
        """Инициализация класса."""
        super().__init__(SPAWN_POS, tilemaps.FOURTH)
