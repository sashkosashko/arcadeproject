"""Стартовый экран."""

from game.change_screen import change_screen
from game.components import Dialog
from game.config import sounds, tilemaps
from game.screens import BaseScreen

SPAWN_POS = (150, 220)


class StartScreen(BaseScreen):
    """Стартовый экран."""

    def __init__(self) -> None:
        """Инициализация класса."""
        super().__init__(SPAWN_POS, tilemaps.START)

        self.dialog = Dialog(
            "???",
            "Ахх.. Где я?. Голова раскалывается.. Как я тут оказалась?.",
            sounds.BEGINNING,
            pos=1,
        )

    def check_change_level(self) -> None:
        """Проверка события переключения между уровнями."""
        if self.player.center_x > 2506 and self.player.center_y < 2576:
            change_screen("1")
