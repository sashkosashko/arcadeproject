"""Первый уровень."""

from random import randint

import arcade

from game import config
from game.change_screen import change_screen
from game.components import Dialog
from game.config import sounds, textures, tilemaps
from game.screens import BaseScreen

SPAWN_POS = 5 + 1 * 32 * config.TILE_SCALING, 6 + 1 * 32 * config.TILE_SCALING


class FirstLevelScreen(BaseScreen):
    """Первый уровень."""

    def __init__(self) -> None:
        """Инициализация класса."""
        super().__init__(SPAWN_POS, tilemaps.LEVEL)

        self.dialog = Dialog(
            "Лиза",
            "Кажется не стоит наступать на синие кружочки!..",
            sounds.BLUE_CROSSES,
            pos=1,
        )

        for i in range(1, 7):
            x = i * 4
            for _ in range(randint(3, 6)):
                y = randint(2, 11)

                self.trial_list.append(
                    arcade.Sprite(
                        arcade.load_texture(textures.BLUE_MINE),
                        config.TILE_SCALING,
                        x * 32 * config.TILE_SCALING + 16 * config.TILE_SCALING,
                        y * 32 * config.TILE_SCALING + 16 * config.TILE_SCALING,
                    ),
                )

    def check_change_level(self) -> None:
        """Проверка события переключения между уровнями."""
        if self.player.center_x > 31 * 32 * config.TILE_SCALING:
            change_screen("2")
