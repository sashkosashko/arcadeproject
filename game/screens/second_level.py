"""Первый уровень."""

from random import randint

import arcade

from game import config
from game.change_screen import change_screen
from game.components import Dialog
from game.config import sounds, textures, tilemaps
from game.screens import BaseScreen

SPAWN_POS = 5 + 1 * 32 * config.TILE_SCALING, 6 + 1 * 32 * config.TILE_SCALING


class SecondLevelScreen(BaseScreen):
    """Первый уровень."""

    def __init__(self) -> None:
        """Инициализация класса."""
        super().__init__(SPAWN_POS, tilemaps.SECOND)

        self.dialog = Dialog(
            "Лиза",
            "Кажется не стоит наступать на синие кружочки!..",
            sounds.BLUE_CROSSES,
            pos=1,
        )

        self.mines = []
        for i in range(1, 7):
            y = 1
            for _ in range(5):
                y += 2
                for _ in range(2):
                    x = randint(1, 3) + 4 * (i - 1)
                    self.mines.append((x, y))

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

        if (
            self.player.center_x / 32 // config.TILE_SCALING,
            self.player.center_y / 32 // config.TILE_SCALING,
        ) in self.mines:
            change_screen("1")
