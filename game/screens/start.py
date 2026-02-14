"""Стартовый экран."""

from game import config
from game.change_screen import change_screen
from game.components import Dialog
from game.config import sounds, tilemaps
from game.screens import BaseScreen
from game.utils.manage_time import save_time

SPAWN_POS = 2, 2


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

    def check_change_level(self) -> None:
        """Проверка события переключения между уровнями."""
        if self.player.center_x > (25 + 1) * 32 * config.TILE_SCALING:
            change_screen("1")
