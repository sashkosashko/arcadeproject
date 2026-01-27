"""Первый уровень."""

from game.change_screen import change_screen
from game.components import Dialog
from game.config import sounds, tilemaps
from game.screens import BaseScreen

SPAWN_POS = 1540, 280


class FirstLevelScreen(BaseScreen):
    """Первый уровень."""

    def __init__(self) -> None:
        """Инициализация класса."""
        super().__init__(SPAWN_POS, tilemaps.FIRST_LEVEL)

        self.dialog = Dialog(
            "Лиза",
            "Ура!..",
            sounds.HOORAY,
            pos=1,
        )

    def check_change_level(self) -> None:
        """Проверка события переключения между уровнями."""
        if (
            self.player.center_x > 1436
            and self.player.center_x < 1816
            and self.player.center_y > 3002
            and self.player.center_y < 3292
        ):
            change_screen("2")
