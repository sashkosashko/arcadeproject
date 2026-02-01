"""Стартовый экран."""

from random import randint

import arcade

from game import config
from game.change_screen import change_screen
from game.components import Dialog
from game.config import sounds, tilemaps, textures
from game.screens import BaseScreen
from game.utils.manage_time import save_time

SPAWN_POS = 150, 220


class StartScreen(BaseScreen):
    """Стартовый экран."""

    def __init__(self) -> None:
        """Инициализация класса."""
        super().__init__(SPAWN_POS, tilemaps.START)

        save_time()

        self.dialog = Dialog(
            "???",
            "Ахх.. Где я?. Голова раскалывается.. Как я тут оказалась?.",
            sounds.BEGINNING,
            pos=1,
        )
        #клетки маршрута в которых уже был звук
        self.sounded = set()

        #Генерация маршрута
        self.mines = []
        x = 8
        y = randint(1, 8)
        self.mines.append((x, y))
        self.trial_list.append(
            arcade.Sprite(
                arcade.load_texture(textures.RED_MINE),
                config.TILE_SCALING,
                x * 32 * config.TILE_SCALING + 16 * config.TILE_SCALING,
                y * 32 * config.TILE_SCALING + 16 * config.TILE_SCALING,
            ),
        )
        while x < 23:
            chance = randint(1, 5)
            if chance == 1:
                x += 1
            elif chance in (2, 3):
                y += 1
            elif chance in (4, 5):
                y -= 1
            if y < 1:
                y = 1
            if y > 8:
                y = 8
            self.mines.append((x, y))
            self.trial_list.append(
                arcade.Sprite(
                    arcade.load_texture(textures.RED_MINE),
                    config.TILE_SCALING,
                    x * 32 * config.TILE_SCALING + 16 * config.TILE_SCALING,
                    y * 32 * config.TILE_SCALING + 16 * config.TILE_SCALING,
                ),
            )

    def check_change_level(self) -> None:
        """Проверка события переключения между уровнями."""
        if self.player.center_x > (31 + 1) * 32 * config.TILE_SCALING:
            change_screen("1")

        check_x = self.player.center_x / 32 // config.TILE_SCALING
        check_y = self.player.center_y / 32 // config.TILE_SCALING
        if (check_x, check_y) not in self.mines and 23 >= check_x >= 8:
            change_screen("0")
        else:
            if (check_x, check_y) not in self.sounded and 23 >= check_x >= 8:
                self.sounded.add((check_x, check_y))
                arcade.play_sound(sounds.CORRECT1)
