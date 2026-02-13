"""Уровень на развитие терпения."""

import arcade

from game import config
from game.change_screen import change_screen
from game.components import Dialog
from game.config import sounds, textures, tilemaps
from game.screens import BaseScreen

SPAWN_POS = 5 + 1 * 32 * config.TILE_SCALING, 6 + 1 * 32 * config.TILE_SCALING
_MINED = (
    *range(1, 6),
    *range(7, 10),
    *range(11, 14),
    *range(15, 18),
    *range(19, 22),
    *range(23, 26),
    *range(27, 31),
)


class PatienceLevelScreen(BaseScreen):
    """Уровень на развитие терпения."""

    def __init__(self) -> None:
        """Инициализация класса."""
        super().__init__(SPAWN_POS, tilemaps.LEVEL)

        self.dialog = Dialog(
            "Лиза",
            "Ура!",
            sounds.HOORAY,
            pos=1,
        )

        self.mines = []
        for i in _MINED:
            self.mines.append((i, 6))
            self.trial_list.append(
                arcade.Sprite(
                    arcade.load_texture(textures.RED_MINE),
                    config.TILE_SCALING,
                    i * 32 * config.TILE_SCALING + 16 * config.TILE_SCALING,
                    6 * 32 * config.TILE_SCALING + 16 * config.TILE_SCALING,
                ),
            )

    def check_change_level(self) -> None:
        """Проверка события переключения между уровнями."""
        if self.player.center_x > 31 * 32 * config.TILE_SCALING:
            change_screen("3")

        if (
            self.player.center_x / 32 // config.TILE_SCALING,
            self.player.center_y / 32 // config.TILE_SCALING,
        ) in self.mines and self.player.speed > 3:
            self.player.speed *= 0.96
